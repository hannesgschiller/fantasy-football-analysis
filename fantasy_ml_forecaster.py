#!/usr/bin/env python3
"""
Fantasy Football ML Forecaster
Machine Learning models for player performance prediction and analysis
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import warnings
warnings.filterwarnings('ignore')

class FantasyMLForecaster:
    def __init__(self, analyzer, season):
        """
        Initialize the ML forecaster with historical data
        
        Args:
            analyzer: FantasyFootballAnalyzer instance with loaded data
            season (str): Season year to analyze (e.g., '2024', '2025')
        """
        self.analyzer = analyzer
        self.season = season
        self.positions = ['QB', 'RB', 'WR', 'TE']
        
        # NFL Bye Weeks (2025 season)
        self.bye_weeks = {
            6: ['DET', 'HOU', 'LV', 'TEN'],
            7: ['BUF', 'LAR', 'MIN', 'PHI'],
            8: ['KC', 'LAC'],
            9: ['CLE', 'DAL', 'DEN', 'NYG', 'PIT', 'SF'],
            10: ['BAL', 'CIN', 'NE', 'NYJ'],
            11: ['JAX', 'MIA', 'SEA', 'TB'],
            12: [],
            13: ['ARI', 'CAR'],
            14: ['ATL', 'CHI', 'GB', 'IND', 'NO', 'WAS']
        }
        
        # Team abbreviation mapping for matching
        self.team_abbrev_map = {
            'BAL': 'BAL', 'CIN': 'CIN', 'CLE': 'CLE', 'PIT': 'PIT',  # AFC North
            'HOU': 'HOU', 'IND': 'IND', 'JAX': 'JAX', 'TEN': 'TEN',  # AFC South
            'BUF': 'BUF', 'MIA': 'MIA', 'NE': 'NE', 'NYJ': 'NYJ',   # AFC East
            'DEN': 'DEN', 'KC': 'KC', 'LAC': 'LAC', 'LV': 'LV',      # AFC West
            'DAL': 'DAL', 'NYG': 'NYG', 'PHI': 'PHI', 'WAS': 'WAS',  # NFC East
            'CHI': 'CHI', 'DET': 'DET', 'GB': 'GB', 'MIN': 'MIN',    # NFC North
            'ATL': 'ATL', 'CAR': 'CAR', 'NO': 'NO', 'TB': 'TB',      # NFC South
            'ARI': 'ARI', 'LAR': 'LAR', 'SF': 'SF', 'SEA': 'SEA'     # NFC West
        }
    
    def _extract_team(self, player_full_name):
        """Extract team abbreviation from player name like 'Player Name (TEAM)'"""
        if '(' in player_full_name and ')' in player_full_name:
            team = player_full_name.split('(')[1].split(')')[0].strip()
            return team.upper()
        return None
    
    def _is_bye_week(self, team, week_num):
        """Check if a team has a bye in a specific week"""
        if week_num in self.bye_weeks:
            return team in self.bye_weeks[week_num]
        return False
        
    def prepare_player_data(self, player_name, position, exclude_byes=True):
        """
        Extract time series data for a specific player, optionally excluding bye weeks
        
        Args:
            player_name (str): Player name (without team)
            position (str): Player position
            exclude_byes (bool): If True, skip weeks where player's team had a bye
            
        Returns:
            pd.DataFrame: Weekly performance data (excluding bye weeks if requested)
        """
        weekly_scores = []
        week_numbers = []
        player_team = None
        
        if self.season not in self.analyzer.weekly_data:
            return pd.DataFrame()
        
        # Sort weeks by extracting the numeric part properly
        week_names = list(self.analyzer.weekly_data[self.season].keys())
        
        # Custom sort to handle "Week 1", "Week 10", etc.
        def extract_week_num(week_name):
            # Extract number from formats like "Week 1", "Week 10", etc.
            parts = week_name.split()
            if len(parts) >= 2:
                try:
                    return int(parts[1])
                except:
                    return 0
            return 0
        
        sorted_weeks = sorted(week_names, key=extract_week_num)
        
        for week_name in sorted_weeks:
            if position in self.analyzer.weekly_data[self.season][week_name]:
                df = self.analyzer.weekly_data[self.season][week_name][position]
                player_row = df[df['Player'].str.contains(player_name, na=False, case=False)]
                
                if not player_row.empty:
                    # Extract week number properly
                    week_num = extract_week_num(week_name)
                    
                    if week_num > 0:
                        # Get player's team on first match
                        if player_team is None:
                            player_team = self._extract_team(player_row.iloc[0]['Player'])
                        
                        # Skip if this is a bye week for the player's team
                        if exclude_byes and player_team and self._is_bye_week(player_team, week_num):
                            continue
                        
                        # Only include non-zero scores (or include all if not a bye)
                        fpts = player_row.iloc[0]['FPTS']
                        if fpts > 0 or not exclude_byes:
                            week_numbers.append(week_num)
                            weekly_scores.append(fpts)
        
        if not weekly_scores:
            return pd.DataFrame()
        
        return pd.DataFrame({
            'week': week_numbers,
            'fpts': weekly_scores
        })
    
    def forecast_next_week(self, player_name, position, method='simple'):
        """
        Forecast next week's performance for a player
        
        Args:
            player_name (str): Player name
            position (str): Player position
            method (str): 'simple' for moving average, 'prophet' for advanced
            
        Returns:
            dict: {predicted_fpts, lower_bound, upper_bound, confidence}
        """
        player_data = self.prepare_player_data(player_name, position)
        
        if player_data.empty or len(player_data) < 3:
            return None
        
        # Simple moving average forecast (fallback)
        if method == 'simple' or len(player_data) < 5:
            recent_avg = player_data['fpts'].tail(3).mean()
            season_std = player_data['fpts'].std()
            
            return {
                'predicted_fpts': round(recent_avg, 1),
                'lower_bound': round(max(0, recent_avg - 1.5 * season_std), 1),
                'upper_bound': round(recent_avg + 1.5 * season_std, 1),
                'confidence': 0.75,
                'method': 'moving_average'
            }
        
        # Advanced Prophet forecast
        try:
            from prophet import Prophet
            
            # Prepare data for Prophet
            prophet_df = pd.DataFrame({
                'ds': pd.date_range(start='2024-09-01', periods=len(player_data), freq='W'),
                'y': player_data['fpts'].values
            })
            
            # Fit model
            model = Prophet(
                yearly_seasonality=False,
                weekly_seasonality=False,
                daily_seasonality=False,
                changepoint_prior_scale=0.05
            )
            model.fit(prophet_df)
            
            # Forecast next week
            future = model.make_future_dataframe(periods=1, freq='W')
            forecast = model.predict(future)
            
            next_week = forecast.iloc[-1]
            
            return {
                'predicted_fpts': round(next_week['yhat'], 1),
                'lower_bound': round(max(0, next_week['yhat_lower']), 1),
                'upper_bound': round(next_week['yhat_upper'], 1),
                'confidence': 0.85,
                'method': 'prophet'
            }
        except Exception as e:
            # Fallback to simple method
            return self.forecast_next_week(player_name, position, method='simple')
    
    def forecast_season_end(self, player_name, position, total_weeks=18):
        """
        Project season-end total for a player
        
        Args:
            player_name (str): Player name
            position (str): Player position
            total_weeks (int): Total weeks in season
            
        Returns:
            dict: {current_total, projected_total, weeks_remaining}
        """
        player_data = self.prepare_player_data(player_name, position)
        
        if player_data.empty:
            return None
        
        current_total = player_data['fpts'].sum()
        weeks_played = len(player_data)
        weeks_remaining = total_weeks - weeks_played
        
        if weeks_remaining <= 0:
            return {
                'current_total': round(current_total, 1),
                'projected_total': round(current_total, 1),
                'weeks_remaining': 0,
                'avg_per_week': round(current_total / weeks_played, 1)
            }
        
        # Use recent performance (last 5 weeks or all available)
        recent_weeks = min(5, weeks_played)
        recent_avg = player_data['fpts'].tail(recent_weeks).mean()
        
        projected_remaining = recent_avg * weeks_remaining
        projected_total = current_total + projected_remaining
        
        return {
            'current_total': round(current_total, 1),
            'projected_total': round(projected_total, 1),
            'weeks_remaining': weeks_remaining,
            'avg_per_week': round(recent_avg, 1)
        }
    
    def identify_breakout_players(self, position, threshold=0.15, min_weeks=5):
        """
        Identify players trending upward (potential breakouts)
        
        Args:
            position (str): Position to analyze
            threshold (float): Minimum improvement threshold (default 15%)
            min_weeks (int): Minimum weeks of data required
            
        Returns:
            pd.DataFrame: Players with breakout potential
        """
        breakout_candidates = []
        
        # Get all players for this position
        season_df = None
        if self.season in self.analyzer.season_data and position in self.analyzer.season_data[self.season]:
            season_df = self.analyzer.season_data[self.season][position]
        else:
            # Use weekly data as fallback
            season_df = self._get_top_from_weekly(position, top_n=50)
        
        if season_df is None or season_df.empty:
            return pd.DataFrame()
        
        for _, row in season_df.iterrows():
            player_name = row['Player'].split(' (')[0]
            player_data = self.prepare_player_data(player_name, position)
            
            if len(player_data) < min_weeks:
                continue
            
            # Compare recent performance vs season average
            season_avg = player_data['fpts'].mean()
            recent_avg = player_data['fpts'].tail(3).mean()
            
            improvement = (recent_avg - season_avg) / season_avg if season_avg > 0 else 0
            
            if improvement >= threshold:
                # Calculate trend slope
                trend_slope = self._calculate_trend_slope(player_data['fpts'].values)
                
                breakout_candidates.append({
                    'Player': row['Player'],
                    'Season_Avg': round(season_avg, 1),
                    'Recent_Avg': round(recent_avg, 1),
                    'Improvement': round(improvement * 100, 1),
                    'Trend_Slope': round(trend_slope, 2),
                    'Momentum_Score': round(improvement * trend_slope * 100, 1)
                })
        
        if breakout_candidates:
            df = pd.DataFrame(breakout_candidates)
            return df.sort_values('Momentum_Score', ascending=False)
        
        return pd.DataFrame()
    
    def identify_bust_risks(self, position, threshold=-0.15, min_weeks=5):
        """
        Identify players trending downward (bust risks)
        
        Args:
            position (str): Position to analyze
            threshold (float): Minimum decline threshold (default -15%)
            min_weeks (int): Minimum weeks of data required
            
        Returns:
            pd.DataFrame: Players with bust risk
        """
        bust_risks = []
        
        # Get all players for this position
        season_df = None
        if self.season in self.analyzer.season_data and position in self.analyzer.season_data[self.season]:
            season_df = self.analyzer.season_data[self.season][position]
        else:
            # Use weekly data as fallback
            season_df = self._get_top_from_weekly(position, top_n=50)
        
        if season_df is None or season_df.empty:
            return pd.DataFrame()
        
        for _, row in season_df.iterrows():
            player_name = row['Player'].split(' (')[0]
            player_data = self.prepare_player_data(player_name, position)
            
            if len(player_data) < min_weeks:
                continue
            
            # Compare recent performance vs season average
            season_avg = player_data['fpts'].mean()
            recent_avg = player_data['fpts'].tail(3).mean()
            
            decline = (recent_avg - season_avg) / season_avg if season_avg > 0 else 0
            
            if decline <= threshold:
                # Calculate trend slope
                trend_slope = self._calculate_trend_slope(player_data['fpts'].values)
                
                bust_risks.append({
                    'Player': row['Player'],
                    'Season_Avg': round(season_avg, 1),
                    'Recent_Avg': round(recent_avg, 1),
                    'Decline': round(decline * 100, 1),
                    'Trend_Slope': round(trend_slope, 2),
                    'Risk_Score': round(abs(decline * trend_slope * 100), 1)
                })
        
        if bust_risks:
            df = pd.DataFrame(bust_risks)
            return df.sort_values('Risk_Score', ascending=False)
        
        return pd.DataFrame()
    
    def calculate_volatility_score(self, player_name, position):
        """
        Calculate volatility/risk score for a player
        
        Args:
            player_name (str): Player name
            position (str): Player position
            
        Returns:
            dict: Volatility metrics
        """
        player_data = self.prepare_player_data(player_name, position)
        
        if player_data.empty or len(player_data) < 3:
            return None
        
        avg_fpts = player_data['fpts'].mean()
        std_fpts = player_data['fpts'].std()
        min_fpts = player_data['fpts'].min()
        max_fpts = player_data['fpts'].max()
        
        # Coefficient of variation (lower = more consistent)
        cv = (std_fpts / avg_fpts) if avg_fpts > 0 else 0
        
        # Consistency score (higher = more consistent)
        consistency_score = avg_fpts / (std_fpts + 1)
        
        # Volatility rating
        if cv < 0.3:
            volatility_rating = "Low"
        elif cv < 0.5:
            volatility_rating = "Medium"
        else:
            volatility_rating = "High"
        
        return {
            'avg_fpts': round(avg_fpts, 1),
            'std_fpts': round(std_fpts, 1),
            'min_fpts': round(min_fpts, 1),
            'max_fpts': round(max_fpts, 1),
            'coefficient_variation': round(cv, 2),
            'consistency_score': round(consistency_score, 2),
            'volatility_rating': volatility_rating
        }
    
    def predict_player_category(self, position, min_weeks=5):
        """
        Classify players into categories using ML
        
        Args:
            position (str): Position to analyze
            min_weeks (int): Minimum weeks of data
            
        Returns:
            pd.DataFrame: Players with categories and scores
        """
        player_categories = []
        
        # Get all players for this position
        season_df = None
        if self.season in self.analyzer.season_data and position in self.analyzer.season_data[self.season]:
            season_df = self.analyzer.season_data[self.season][position]
        else:
            # Use weekly data as fallback
            season_df = self._get_top_from_weekly(position, top_n=50)
        
        if season_df is None or season_df.empty:
            return pd.DataFrame()
        
        for _, row in season_df.iterrows():
            player_name = row['Player'].split(' (')[0]
            player_data = self.prepare_player_data(player_name, position)
            
            if len(player_data) < min_weeks:
                continue
            
            # Calculate features
            avg_fpts = player_data['fpts'].mean()
            std_fpts = player_data['fpts'].std()
            trend_slope = self._calculate_trend_slope(player_data['fpts'].values)
            recent_avg = player_data['fpts'].tail(3).mean()
            cv = (std_fpts / avg_fpts) if avg_fpts > 0 else 0
            
            # Classify based on rules
            category = self._classify_player(avg_fpts, cv, trend_slope, position)
            recommendation = self._get_recommendation(category, trend_slope, cv)
            
            player_categories.append({
                'Player': row['Player'],
                'Avg_FPTS': round(avg_fpts, 1),
                'Volatility': round(cv, 2),
                'Trend': round(trend_slope, 2),
                'Category': category,
                'Recommendation': recommendation
            })
        
        if player_categories:
            return pd.DataFrame(player_categories)
        
        return pd.DataFrame()
    
    def _calculate_trend_slope(self, weekly_scores):
        """Calculate trend using linear regression"""
        if len(weekly_scores) < 3:
            return 0
        
        X = np.arange(len(weekly_scores)).reshape(-1, 1)
        y = np.array(weekly_scores)
        
        model = LinearRegression()
        model.fit(X, y)
        
        return model.coef_[0]
    
    def _classify_player(self, avg_fpts, cv, trend_slope, position):
        """Classify player based on performance metrics"""
        # Position-specific thresholds
        thresholds = {
            'QB': {'elite': 20, 'good': 15},
            'RB': {'elite': 15, 'good': 10},
            'WR': {'elite': 12, 'good': 8},
            'TE': {'elite': 9, 'good': 6}
        }
        
        elite_threshold = thresholds.get(position, {}).get('elite', 15)
        good_threshold = thresholds.get(position, {}).get('good', 10)
        
        # Classification logic
        if avg_fpts >= elite_threshold and cv < 0.4:
            return "Elite"
        elif avg_fpts >= good_threshold and cv < 0.5:
            if trend_slope > 0.5:
                return "Rising Star"
            else:
                return "Consistent"
        elif cv > 0.6:
            return "Volatile"
        elif trend_slope < -0.5:
            return "Declining"
        else:
            return "Average"
    
    def _get_recommendation(self, category, trend_slope, cv):
        """Get actionable recommendation based on category"""
        if category == "Elite":
            return "HOLD - Top Tier"
        elif category == "Rising Star":
            return "BUY - Trending Up"
        elif category == "Consistent":
            return "HOLD - Reliable"
        elif category == "Volatile":
            if trend_slope > 0:
                return "RISKY - High Ceiling"
            else:
                return "SELL - Unpredictable"
        elif category == "Declining":
            return "SELL - Trending Down"
        else:
            return "HOLD - Monitor"
    
    def calculate_momentum_score(self, player_name, position):
        """
        Calculate momentum score based on recent vs season performance
        
        Args:
            player_name (str): Player name
            position (str): Player position
            
        Returns:
            float: Momentum score (positive = trending up)
        """
        player_data = self.prepare_player_data(player_name, position)
        
        if player_data.empty or len(player_data) < 5:
            return 0
        
        season_avg = player_data['fpts'].mean()
        recent_avg = player_data['fpts'].tail(3).mean()
        
        momentum = (recent_avg - season_avg) / season_avg if season_avg > 0 else 0
        
        return round(momentum * 100, 1)
    
    def get_all_player_forecasts(self, position, top_n=10):
        """
        Get forecasts for all top players at a position
        
        Args:
            position (str): Position to analyze
            top_n (int): Number of players to forecast
            
        Returns:
            pd.DataFrame: Forecast data for top players
        """
        forecasts = []
        
        # Try to get top performers from season data first
        top_players = self.analyzer.get_top_performers(position, week=None, top_n=top_n, season=self.season)
        
        # If no season data, calculate from weekly data
        if top_players is None or top_players.empty:
            top_players = self._get_top_from_weekly(position, top_n)
        
        if top_players is None or top_players.empty:
            return pd.DataFrame()
        
        for _, row in top_players.iterrows():
            player_name = row['Player'].split(' (')[0] if '(' in row['Player'] else row['Player']
            
            # Get forecast
            forecast = self.forecast_next_week(player_name, position)
            
            if forecast:
                current_avg = row.get('FPTS/G', row.get('Avg_FPTS', forecast['predicted_fpts']))
                forecasts.append({
                    'Player': row['Player'],
                    'Current_Avg': round(current_avg, 1),
                    'Next_Week_Pred': forecast['predicted_fpts'],
                    'Confidence_Low': forecast['lower_bound'],
                    'Confidence_High': forecast['upper_bound'],
                    'Trend': '↑' if forecast['predicted_fpts'] > current_avg else '↓'
                })
        
        if forecasts:
            return pd.DataFrame(forecasts)
        
        return pd.DataFrame()
    
    def _get_top_from_weekly(self, position, top_n=10):
        """
        Calculate top performers from weekly data when season data is not available
        
        Args:
            position (str): Position to analyze
            top_n (int): Number of top players to return
            
        Returns:
            pd.DataFrame: Top performers calculated from weekly averages
        """
        if self.season not in self.analyzer.weekly_data:
            print(f"DEBUG: Season {self.season} not in weekly_data")
            return pd.DataFrame()
        
        player_stats = {}
        weeks_processed = 0
        
        # Aggregate all weekly data
        for week_name in self.analyzer.weekly_data[self.season].keys():
            if position in self.analyzer.weekly_data[self.season][week_name]:
                df = self.analyzer.weekly_data[self.season][week_name][position]
                weeks_processed += 1
                
                for _, row in df.iterrows():
                    player = row['Player']
                    fpts = row.get('FPTS', 0)
                    
                    if player not in player_stats:
                        player_stats[player] = {'total': 0, 'count': 0, 'scores': []}
                    
                    player_stats[player]['total'] += fpts
                    player_stats[player]['count'] += 1
                    player_stats[player]['scores'].append(fpts)
        
        print(f"DEBUG: Processed {weeks_processed} weeks, found {len(player_stats)} players")
        
        # Create summary DataFrame
        summary_data = []
        for player, stats in player_stats.items():
            if stats['count'] > 0:
                summary_data.append({
                    'Player': player,
                    'FPTS': stats['total'],
                    'FPTS/G': stats['total'] / stats['count'],
                    'Avg_FPTS': stats['total'] / stats['count']
                })
        
        print(f"DEBUG: Created summary for {len(summary_data)} players")
        
        if summary_data:
            df = pd.DataFrame(summary_data)
            result = df.nlargest(top_n, 'FPTS')
            print(f"DEBUG: Returning top {len(result)} players")
            return result
        
        return pd.DataFrame()
    
    def get_risk_assessment(self, position):
        """
        Get comprehensive risk assessment for all players at a position
        
        Args:
            position (str): Position to analyze
            
        Returns:
            pd.DataFrame: Risk metrics for all players
        """
        risk_data = []
        
        # Get all players for this position
        season_df = None
        if self.season in self.analyzer.season_data and position in self.analyzer.season_data[self.season]:
            season_df = self.analyzer.season_data[self.season][position]
        else:
            # Use weekly data as fallback
            season_df = self._get_top_from_weekly(position, top_n=50)
        
        if season_df is None or season_df.empty:
            return pd.DataFrame()
        
        for _, row in season_df.iterrows():
            player_name = row['Player'].split(' (')[0]
            volatility = self.calculate_volatility_score(player_name, position)
            
            if volatility:
                risk_data.append({
                    'Player': row['Player'],
                    'Avg_FPTS': volatility['avg_fpts'],
                    'Volatility': volatility['coefficient_variation'],
                    'Volatility_Rating': volatility['volatility_rating'],
                    'Consistency_Score': volatility['consistency_score'],
                    'Floor': volatility['min_fpts'],
                    'Ceiling': volatility['max_fpts']
                })
        
        if risk_data:
            return pd.DataFrame(risk_data)
        
        return pd.DataFrame()

def calculate_trend_slope(weekly_scores):
    """Helper function to calculate trend slope"""
    if len(weekly_scores) < 3:
        return 0
    
    X = np.arange(len(weekly_scores)).reshape(-1, 1)
    y = np.array(weekly_scores)
    
    model = LinearRegression()
    model.fit(X, y)
    
    return model.coef_[0]

def calculate_momentum_score(recent_weeks, season_avg):
    """Calculate momentum score"""
    if season_avg == 0:
        return 0
    
    recent_avg = np.mean(recent_weeks)
    momentum = (recent_avg - season_avg) / season_avg
    
    return momentum * 100

