#!/usr/bin/env python3
"""
Fantasy Football Analysis Tool
Analyzes weekly and season-long fantasy football data from FantasyPros
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import glob
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

class FantasyFootballAnalyzer:
    def __init__(self, data_path):
        """
        Initialize the analyzer with the path to fantasy football data
        
        Args:
            data_path (str): Path to the folder containing weekly data
        """
        self.data_path = Path(data_path)
        self.positions = ['QB', 'RB', 'WR', 'TE']
        self.weekly_data = {}
        self.season_data = {}
        
    def load_weekly_data(self):
        """Load all weekly data for all positions"""
        print("Loading weekly fantasy football data...")
        
        # Find all week folders
        week_folders = sorted([f for f in self.data_path.iterdir() 
                              if f.is_dir() and f.name.startswith('Week')])
        
        for week_folder in week_folders:
            week_num = week_folder.name
            self.weekly_data[week_num] = {}
            
            for position in self.positions:
                # Look for position-specific CSV files
                pattern = f"*{position}*.csv"
                files = list(week_folder.glob(pattern))
                
                if files:
                    try:
                        df = pd.read_csv(files[0])
                        # Clean column names
                        df.columns = df.columns.str.strip().str.replace('"', '')
                        self.weekly_data[week_num][position] = df
                        print(f"Loaded {position} data for {week_num}")
                    except Exception as e:
                        print(f"Error loading {position} data for {week_num}: {e}")
        
        print(f"Loaded data for {len(self.weekly_data)} weeks")
        
    def load_season_data(self):
        """Load season-long aggregated data"""
        print("Loading season-long data...")
        
        season_folder = self.data_path / "Full Season"
        if season_folder.exists():
            for position in self.positions:
                pattern = f"*{position}*.csv"
                files = list(season_folder.glob(pattern))
                
                if files:
                    try:
                        df = pd.read_csv(files[0])
                        df.columns = df.columns.str.strip().str.replace('"', '')
                        self.season_data[position] = df
                        print(f"Loaded season {position} data")
                    except Exception as e:
                        print(f"Error loading season {position} data: {e}")
    
    def get_top_performers(self, position, week=None, top_n=10):
        """
        Get top performers for a specific position and week
        
        Args:
            position (str): Position (QB, RB, WR, TE)
            week (str): Week number (e.g., 'Week 1') or None for season
            top_n (int): Number of top performers to return
        """
        if week:
            if week in self.weekly_data and position in self.weekly_data[week]:
                df = self.weekly_data[week][position]
            else:
                return None
        else:
            if position in self.season_data:
                df = self.season_data[position]
            else:
                return None
        
        # Sort by fantasy points
        if 'FPTS' in df.columns:
            return df.nlargest(top_n, 'FPTS')[['Player', 'FPTS', 'FPTS/G']]
        return None
    
    def analyze_position_trends(self, position, metric='FPTS'):
        """
        Analyze trends for a specific position across weeks
        
        Args:
            position (str): Position to analyze
            metric (str): Metric to track (FPTS, FPTS/G, etc.)
        """
        trends = []
        
        for week, week_data in self.weekly_data.items():
            if position in week_data:
                df = week_data[position]
                if metric in df.columns:
                    # Get top 5 performers for the week
                    top_5 = df.nlargest(5, metric)
                    for _, row in top_5.iterrows():
                        trends.append({
                            'Week': week,
                            'Player': row['Player'],
                            metric: row[metric],
                            'Rank': row.get('Rank', 'N/A')
                        })
        
        return pd.DataFrame(trends)
    
    def get_consistency_analysis(self, position, min_games=3):
        """
        Analyze player consistency across weeks
        
        Args:
            position (str): Position to analyze
            min_games (int): Minimum games played to be included
        """
        player_stats = {}
        
        for week, week_data in self.weekly_data.items():
            if position in week_data:
                df = week_data[position]
                for _, row in df.iterrows():
                    player = row['Player']
                    fpts = row.get('FPTS', 0)
                    
                    if player not in player_stats:
                        player_stats[player] = {'weeks': [], 'fpts': []}
                    
                    player_stats[player]['weeks'].append(week)
                    player_stats[player]['fpts'].append(fpts)
        
        # Calculate consistency metrics
        consistency_data = []
        for player, stats in player_stats.items():
            if len(stats['weeks']) >= min_games:
                fpts_array = np.array(stats['fpts'])
                consistency_data.append({
                    'Player': player,
                    'Games_Played': len(stats['weeks']),
                    'Avg_FPTS': np.mean(fpts_array),
                    'Std_FPTS': np.std(fpts_array),
                    'Min_FPTS': np.min(fpts_array),
                    'Max_FPTS': np.max(fpts_array),
                    'Consistency_Score': np.mean(fpts_array) / (np.std(fpts_array) + 1)  # Higher is more consistent
                })
        
        return pd.DataFrame(consistency_data).sort_values('Consistency_Score', ascending=False)
    
    def create_weekly_summary(self, week):
        """
        Create a summary of top performers for a specific week
        
        Args:
            week (str): Week to analyze (e.g., 'Week 1')
        """
        if week not in self.weekly_data:
            return None
        
        summary = {}
        for position in self.positions:
            if position in self.weekly_data[week]:
                df = self.weekly_data[week][position]
                top_3 = df.nlargest(3, 'FPTS')[['Player', 'FPTS']]
                summary[position] = top_3
        
        return summary
    
    def plot_position_comparison(self, week=None):
        """
        Create a comparison plot of top performers across positions
        
        Args:
            week (str): Week to analyze or None for season
        """
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle(f'Top 10 Performers by Position - {week if week else "Season"}', fontsize=16)
        
        for i, position in enumerate(self.positions):
            ax = axes[i//2, i%2]
            
            top_performers = self.get_top_performers(position, week, top_n=10)
            if top_performers is not None:
                # Extract player names (remove team info)
                players = [p.split(' (')[0] if ' (' in p else p for p in top_performers['Player']]
                fpts = top_performers['FPTS']
                
                bars = ax.barh(range(len(players)), fpts, color=f'C{i}')
                ax.set_yticks(range(len(players)))
                ax.set_yticklabels(players)
                ax.set_xlabel('Fantasy Points')
                ax.set_title(f'{position} Top Performers')
                ax.invert_yaxis()
                
                # Add value labels on bars
                for j, (bar, value) in enumerate(zip(bars, fpts)):
                    ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2, 
                           f'{value:.1f}', va='center')
        
        plt.tight_layout()
        return fig
    
    def plot_weekly_trends(self, position, top_n=5):
        """
        Plot weekly trends for top performers in a position
        
        Args:
            position (str): Position to analyze
            top_n (int): Number of top players to track
        """
        # Get top players for the season
        season_top = self.get_top_performers(position, week=None, top_n=top_n)
        if season_top is None:
            return None
        
        top_players = [p.split(' (')[0] if ' (' in p else p for p in season_top['Player']]
        
        # Track their weekly performance
        weekly_performance = {}
        for player in top_players:
            weekly_performance[player] = []
        
        weeks = sorted(self.weekly_data.keys())
        for week in weeks:
            if position in self.weekly_data[week]:
                df = self.weekly_data[week][position]
                for player in top_players:
                    # Find player in this week's data
                    player_row = df[df['Player'].str.contains(player, na=False)]
                    if not player_row.empty:
                        weekly_performance[player].append(player_row.iloc[0]['FPTS'])
                    else:
                        weekly_performance[player].append(0)
        
        # Create the plot
        fig, ax = plt.subplots(figsize=(12, 8))
        
        for player, performance in weekly_performance.items():
            ax.plot(range(1, len(performance) + 1), performance, marker='o', label=player, linewidth=2)
        
        ax.set_xlabel('Week')
        ax.set_ylabel('Fantasy Points')
        ax.set_title(f'{position} Weekly Performance Trends - Top {top_n} Season Performers')
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def generate_report(self, output_file='fantasy_football_report.html'):
        """
        Generate a comprehensive HTML report
        
        Args:
            output_file (str): Output file name
        """
        html_content = """
        <html>
        <head>
            <title>Fantasy Football Analysis Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                h1, h2, h3 { color: #333; }
                .section { margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }
                table { border-collapse: collapse; width: 100%; margin: 10px 0; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
                .highlight { background-color: #fff3cd; }
            </style>
        </head>
        <body>
            <h1>Fantasy Football Analysis Report</h1>
        """
        
        # Season Summary
        html_content += """
            <div class="section">
                <h2>Season Summary</h2>
        """
        
        for position in self.positions:
            top_performers = self.get_top_performers(position, week=None, top_n=5)
            if top_performers is not None:
                html_content += f"<h3>Top 5 {position}s (Season)</h3>"
                html_content += top_performers.to_html(index=False, classes='table')
        
        # Weekly Analysis
        html_content += """
            </div>
            <div class="section">
                <h2>Weekly Analysis</h2>
        """
        
        for week in sorted(self.weekly_data.keys()):
            summary = self.create_weekly_summary(week)
            if summary:
                html_content += f"<h3>{week}</h3>"
                for position, data in summary.items():
                    html_content += f"<h4>Top 3 {position}s</h4>"
                    html_content += data.to_html(index=False, classes='table')
        
        # Consistency Analysis
        html_content += """
            </div>
            <div class="section">
                <h2>Consistency Analysis</h2>
        """
        
        for position in self.positions:
            consistency = self.get_consistency_analysis(position)
            if not consistency.empty:
                html_content += f"<h3>Most Consistent {position}s</h3>"
                html_content += consistency.head(10).to_html(index=False, classes='table')
        
        html_content += """
            </div>
        </body>
        </html>
        """
        
        with open(output_file, 'w') as f:
            f.write(html_content)
        
        print(f"Report generated: {output_file}")

def main():
    """Main function to run the analysis"""
    # Initialize analyzer with your data path
    data_path = "/Users/hannesschiller/Documents/NFL Fantasy data"
    analyzer = FantasyFootballAnalyzer(data_path)
    
    # Load data
    analyzer.load_weekly_data()
    analyzer.load_season_data()
    
    # Generate analysis
    print("\n=== FANTASY FOOTBALL ANALYSIS ===\n")
    
    # Show top performers for each position
    for position in analyzer.positions:
        print(f"\n--- Top 10 {position}s (Season) ---")
        top_performers = analyzer.get_top_performers(position, week=None, top_n=10)
        if top_performers is not None:
            print(top_performers.to_string(index=False))
    
    # Show consistency analysis
    print("\n--- Consistency Analysis ---")
    for position in analyzer.positions:
        print(f"\nMost Consistent {position}s:")
        consistency = analyzer.get_consistency_analysis(position)
        if not consistency.empty:
            print(consistency.head(5).to_string(index=False))
    
    # Generate visualizations
    print("\nGenerating visualizations...")
    
    # Position comparison plot
    fig1 = analyzer.plot_position_comparison()
    if fig1:
        fig1.savefig('position_comparison.png', dpi=300, bbox_inches='tight')
        print("Saved: position_comparison.png")
    
    # Weekly trends for each position
    for position in analyzer.positions:
        fig2 = analyzer.plot_weekly_trends(position)
        if fig2:
            fig2.savefig(f'{position}_weekly_trends.png', dpi=300, bbox_inches='tight')
            print(f"Saved: {position}_weekly_trends.png")
    
    # Generate HTML report
    analyzer.generate_report()
    
    print("\nAnalysis complete! Check the generated files for detailed results.")

if __name__ == "__main__":
    main() 