#!/usr/bin/env python3
"""
Advanced Fantasy Football Analysis
Additional insights including breakout players, value analysis, and trends
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from fantasy_analyzer import FantasyFootballAnalyzer
import warnings
warnings.filterwarnings('ignore')

class AdvancedFantasyAnalyzer(FantasyFootballAnalyzer):
    def __init__(self, data_path):
        super().__init__(data_path)
        
    def find_breakout_players(self, position, threshold_improvement=0.5):
        """
        Find players who have significantly improved their performance
        
        Args:
            position (str): Position to analyze
            threshold_improvement (float): Minimum improvement factor
        """
        if position not in self.season_data:
            return None
        
        season_df = self.season_data[position]
        breakout_players = []
        
        for _, player_row in season_df.iterrows():
            player = player_row['Player']
            season_fpts = player_row.get('FPTS', 0)
            season_games = player_row.get('G', 1)
            
            if season_games < 3:  # Need minimum games for meaningful comparison
                continue
            
            # Calculate average performance per game
            avg_fpts = season_fpts / season_games
            
            # Find this player's early season performance (first 3 weeks)
            early_performance = []
            for week in ['Week 1', 'Week 2', 'Week 3']:
                if week in self.weekly_data and position in self.weekly_data[week]:
                    week_df = self.weekly_data[week][position]
                    player_week = week_df[week_df['Player'].str.contains(player.split(' (')[0], na=False)]
                    if not player_week.empty:
                        early_performance.append(player_week.iloc[0]['FPTS'])
            
            if len(early_performance) >= 2:
                early_avg = np.mean(early_performance)
                if early_avg > 0 and avg_fpts > early_avg * (1 + threshold_improvement):
                    breakout_players.append({
                        'Player': player,
                        'Early_Avg_FPTS': early_avg,
                        'Season_Avg_FPTS': avg_fpts,
                        'Improvement_Factor': avg_fpts / early_avg,
                        'Games_Played': season_games
                    })
        
        return pd.DataFrame(breakout_players).sort_values('Improvement_Factor', ascending=False)
    
    def analyze_value_players(self, position, min_games=5):
        """
        Find players who provide good value (high performance relative to roster percentage)
        
        Args:
            position (str): Position to analyze
            min_games (int): Minimum games played
        """
        if position not in self.season_data:
            return None
        
        season_df = self.season_data[position]
        value_players = []
        
        for _, player_row in season_df.iterrows():
            player = player_row['Player']
            fpts = player_row.get('FPTS', 0)
            games = player_row.get('G', 1)
            roster_pct = player_row.get('ROST', '0%')
            
            if games < min_games:
                continue
            
            # Convert roster percentage to float
            try:
                roster_pct_float = float(roster_pct.replace('%', '')) / 100
            except:
                roster_pct_float = 0
            
            if roster_pct_float > 0:
                avg_fpts = fpts / games
                value_score = avg_fpts / roster_pct_float  # Higher is better value
                
                value_players.append({
                    'Player': player,
                    'Avg_FPTS': avg_fpts,
                    'Roster_Percentage': roster_pct_float,
                    'Value_Score': value_score,
                    'Games_Played': games
                })
        
        return pd.DataFrame(value_players).sort_values('Value_Score', ascending=False)
    
    def analyze_weekly_volatility(self, position, top_n=20):
        """
        Analyze which players are most volatile (inconsistent) in their performance
        
        Args:
            position (str): Position to analyze
            top_n (int): Number of top players to analyze
        """
        # Get top players for the season
        season_top = self.get_top_performers(position, week=None, top_n=top_n)
        if season_top is None:
            return None
        
        volatility_data = []
        
        for _, player_row in season_top.iterrows():
            player = player_row['Player']
            player_name = player.split(' (')[0]
            
            # Get weekly performance
            weekly_performance = []
            for week, week_data in self.weekly_data.items():
                if position in week_data:
                    df = week_data[position]
                    player_week = df[df['Player'].str.contains(player_name, na=False)]
                    if not player_week.empty:
                        weekly_performance.append(player_week.iloc[0]['FPTS'])
            
            if len(weekly_performance) >= 3:
                fpts_array = np.array(weekly_performance)
                volatility_data.append({
                    'Player': player,
                    'Avg_FPTS': np.mean(fpts_array),
                    'Std_FPTS': np.std(fpts_array),
                    'Coefficient_of_Variation': np.std(fpts_array) / np.mean(fpts_array),
                    'Min_FPTS': np.min(fpts_array),
                    'Max_FPTS': np.max(fpts_array),
                    'Games_Played': len(weekly_performance)
                })
        
        return pd.DataFrame(volatility_data).sort_values('Coefficient_of_Variation', ascending=False)
    
    def find_emerging_trends(self, position, recent_weeks=3):
        """
        Find players who are trending upward in recent weeks
        
        Args:
            position (str): Position to analyze
            recent_weeks (int): Number of recent weeks to consider
        """
        # Get recent weeks
        all_weeks = sorted(self.weekly_data.keys())
        recent_week_list = all_weeks[-recent_weeks:] if len(all_weeks) >= recent_weeks else all_weeks
        
        trending_players = []
        
        # Get all players who played in recent weeks
        recent_players = set()
        for week in recent_week_list:
            if position in self.weekly_data[week]:
                df = self.weekly_data[week][position]
                recent_players.update(df['Player'].tolist())
        
        for player in recent_players:
            player_name = player.split(' (')[0]
            
            # Get recent performance
            recent_performance = []
            for week in recent_week_list:
                if position in self.weekly_data[week]:
                    df = self.weekly_data[week][position]
                    player_week = df[df['Player'].str.contains(player_name, na=False)]
                    if not player_week.empty:
                        recent_performance.append(player_week.iloc[0]['FPTS'])
            
            if len(recent_performance) >= 2:
                recent_avg = np.mean(recent_performance)
                
                # Compare with earlier performance
                earlier_performance = []
                earlier_weeks = [w for w in all_weeks if w not in recent_week_list]
                for week in earlier_weeks[-3:]:  # Last 3 weeks before recent
                    if position in self.weekly_data[week]:
                        df = self.weekly_data[week][position]
                        player_week = df[df['Player'].str.contains(player_name, na=False)]
                        if not player_week.empty:
                            earlier_performance.append(player_week.iloc[0]['FPTS'])
                
                if earlier_performance:
                    earlier_avg = np.mean(earlier_performance)
                    if earlier_avg > 0 and recent_avg > earlier_avg * 1.2:  # 20% improvement
                        trending_players.append({
                            'Player': player,
                            'Earlier_Avg_FPTS': earlier_avg,
                            'Recent_Avg_FPTS': recent_avg,
                            'Improvement_Percentage': ((recent_avg - earlier_avg) / earlier_avg) * 100,
                            'Recent_Games': len(recent_performance)
                        })
        
        return pd.DataFrame(trending_players).sort_values('Improvement_Percentage', ascending=False)
    
    def create_position_dashboard(self, position):
        """
        Create a comprehensive dashboard for a specific position
        
        Args:
            position (str): Position to analyze
        """
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle(f'{position} Position Dashboard', fontsize=16)
        
        # 1. Top performers
        top_performers = self.get_top_performers(position, week=None, top_n=10)
        if top_performers is not None:
            players = [p.split(' (')[0] if ' (' in p else p for p in top_performers['Player']]
            fpts = top_performers['FPTS']
            
            axes[0, 0].barh(range(len(players)), fpts, color='skyblue')
            axes[0, 0].set_yticks(range(len(players)))
            axes[0, 0].set_yticklabels(players)
            axes[0, 0].set_xlabel('Fantasy Points')
            axes[0, 0].set_title('Top 10 Season Performers')
            axes[0, 0].invert_yaxis()
        
        # 2. Consistency analysis
        consistency = self.get_consistency_analysis(position)
        if not consistency.empty:
            top_consistent = consistency.head(10)
            players = top_consistent['Player']
            consistency_scores = top_consistent['Consistency_Score']
            
            axes[0, 1].barh(range(len(players)), consistency_scores, color='lightgreen')
            axes[0, 1].set_yticks(range(len(players)))
            axes[0, 1].set_yticklabels(players)
            axes[0, 1].set_xlabel('Consistency Score')
            axes[0, 1].set_title('Most Consistent Players')
            axes[0, 1].invert_yaxis()
        
        # 3. Weekly trends
        fig_trends = self.plot_weekly_trends(position, top_n=5)
        if fig_trends:
            # Copy the plot to our dashboard
            for ax in fig_trends.axes:
                axes[1, 0].plot(ax.lines[0].get_xdata(), ax.lines[0].get_ydata(), 
                               label=ax.lines[0].get_label(), marker='o')
            axes[1, 0].set_xlabel('Week')
            axes[1, 0].set_ylabel('Fantasy Points')
            axes[1, 0].set_title('Weekly Performance Trends')
            axes[1, 0].legend()
            axes[1, 0].grid(True, alpha=0.3)
        
        # 4. Value analysis
        value_players = self.analyze_value_players(position)
        if value_players is not None and not value_players.empty:
            top_value = value_players.head(10)
            players = top_value['Player']
            value_scores = top_value['Value_Score']
            
            axes[1, 1].barh(range(len(players)), value_scores, color='gold')
            axes[1, 1].set_yticks(range(len(players)))
            axes[1, 1].set_yticklabels(players)
            axes[1, 1].set_xlabel('Value Score')
            axes[1, 1].set_title('Best Value Players')
            axes[1, 1].invert_yaxis()
        
        plt.tight_layout()
        return fig
    
    def generate_advanced_report(self, output_file='advanced_fantasy_report.html'):
        """
        Generate an advanced HTML report with additional insights
        """
        html_content = """
        <html>
        <head>
            <title>Advanced Fantasy Football Analysis Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
                .container { max-width: 1200px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
                h1, h2, h3 { color: #2c3e50; }
                .section { margin: 20px 0; padding: 20px; border: 1px solid #ddd; border-radius: 8px; background-color: #fafafa; }
                .highlight-section { background-color: #e8f4fd; border-color: #3498db; }
                .warning-section { background-color: #fff3cd; border-color: #ffc107; }
                table { border-collapse: collapse; width: 100%; margin: 10px 0; }
                th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
                th { background-color: #34495e; color: white; }
                tr:nth-child(even) { background-color: #f2f2f2; }
                .metric { font-weight: bold; color: #e74c3c; }
                .positive { color: #27ae60; }
                .negative { color: #e74c3c; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Advanced Fantasy Football Analysis Report</h1>
        """
        
        # Breakout Players
        html_content += """
            <div class="section highlight-section">
                <h2>🚀 Breakout Players</h2>
        """
        
        for position in self.positions:
            breakouts = self.find_breakout_players(position)
            if breakouts is not None and not breakouts.empty:
                html_content += f"<h3>{position} Breakout Players</h3>"
                html_content += breakouts.head(5).to_html(index=False, classes='table')
        
        # Value Players
        html_content += """
            </div>
            <div class="section">
                <h2>💰 Value Players</h2>
        """
        
        for position in self.positions:
            value_players = self.analyze_value_players(position)
            if value_players is not None and not value_players.empty:
                html_content += f"<h3>Best Value {position}s</h3>"
                html_content += value_players.head(5).to_html(index=False, classes='table')
        
        # Volatility Analysis
        html_content += """
            </div>
            <div class="section warning-section">
                <h2>⚠️ Volatility Analysis</h2>
        """
        
        for position in self.positions:
            volatility = self.analyze_weekly_volatility(position)
            if volatility is not None and not volatility.empty:
                html_content += f"<h3>Most Volatile {position}s</h3>"
                html_content += volatility.head(5).to_html(index=False, classes='table')
        
        # Emerging Trends
        html_content += """
            </div>
            <div class="section highlight-section">
                <h2>📈 Emerging Trends</h2>
        """
        
        for position in self.positions:
            trends = self.find_emerging_trends(position)
            if trends is not None and not trends.empty:
                html_content += f"<h3>{position}s on the Rise</h3>"
                html_content += trends.head(5).to_html(index=False, classes='table')
        
        # Consistency Analysis
        html_content += """
            </div>
            <div class="section">
                <h2>🎯 Consistency Analysis</h2>
        """
        
        for position in self.positions:
            consistency = self.get_consistency_analysis(position)
            if not consistency.empty:
                html_content += f"<h3>Most Consistent {position}s</h3>"
                html_content += consistency.head(5).to_html(index=False, classes='table')
        
        html_content += """
            </div>
            </div>
        </body>
        </html>
        """
        
        with open(output_file, 'w') as f:
            f.write(html_content)
        
        print(f"Advanced report generated: {output_file}")

def main():
    """Main function to run advanced analysis"""
    data_path = "/Users/hannesschiller/Documents/NFL Fantasy data"
    analyzer = AdvancedFantasyAnalyzer(data_path)
    
    # Load data
    analyzer.load_weekly_data()
    analyzer.load_season_data()
    
    print("\n=== ADVANCED FANTASY FOOTBALL ANALYSIS ===\n")
    
    # Breakout Players Analysis
    print("--- Breakout Players ---")
    for position in analyzer.positions:
        breakouts = analyzer.find_breakout_players(position)
        if breakouts is not None and not breakouts.empty:
            print(f"\n{position} Breakout Players:")
            print(breakouts.head(3).to_string(index=False))
    
    # Value Players Analysis
    print("\n--- Value Players ---")
    for position in analyzer.positions:
        value_players = analyzer.analyze_value_players(position)
        if value_players is not None and not value_players.empty:
            print(f"\nBest Value {position}s:")
            print(value_players.head(3).to_string(index=False))
    
    # Volatility Analysis
    print("\n--- Volatility Analysis ---")
    for position in analyzer.positions:
        volatility = analyzer.analyze_weekly_volatility(position)
        if volatility is not None and not volatility.empty:
            print(f"\nMost Volatile {position}s:")
            print(volatility.head(3).to_string(index=False))
    
    # Emerging Trends
    print("\n--- Emerging Trends ---")
    for position in analyzer.positions:
        trends = analyzer.find_emerging_trends(position)
        if trends is not None and not trends.empty:
            print(f"\n{position}s on the Rise:")
            print(trends.head(3).to_string(index=False))
    
    # Generate position dashboards
    print("\nGenerating position dashboards...")
    for position in analyzer.positions:
        fig = analyzer.create_position_dashboard(position)
        if fig:
            fig.savefig(f'{position}_dashboard.png', dpi=300, bbox_inches='tight')
            print(f"Saved: {position}_dashboard.png")
    
    # Generate advanced report
    analyzer.generate_advanced_report()
    
    print("\nAdvanced analysis complete!")

if __name__ == "__main__":
    main() 