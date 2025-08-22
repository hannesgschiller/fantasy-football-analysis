#!/usr/bin/env python3
"""
Quick Fantasy Football Analysis
Interactive script for quick queries and analysis
"""

import pandas as pd
from fantasy_analyzer import FantasyFootballAnalyzer
from advanced_analysis import AdvancedFantasyAnalyzer

def quick_analysis():
    """Interactive quick analysis tool"""
    data_path = "/Users/hannesschiller/Documents/NFL Fantasy data"
    
    print("🏈 Fantasy Football Quick Analysis Tool")
    print("=" * 50)
    
    # Initialize analyzer
    analyzer = AdvancedFantasyAnalyzer(data_path)
    analyzer.load_weekly_data()
    analyzer.load_season_data()
    
    while True:
        print("\nChoose an analysis option:")
        print("1. Top performers by position")
        print("2. Weekly summary")
        print("3. Consistency analysis")
        print("4. Breakout players")
        print("5. Value players")
        print("6. Volatility analysis")
        print("7. Emerging trends")
        print("8. Generate all reports")
        print("9. Exit")
        
        choice = input("\nEnter your choice (1-9): ").strip()
        
        if choice == '1':
            position = input("Enter position (QB/RB/WR/TE): ").upper()
            if position in ['QB', 'RB', 'WR', 'TE']:
                top_performers = analyzer.get_top_performers(position, week=None, top_n=10)
                if top_performers is not None:
                    print(f"\nTop 10 {position}s:")
                    print(top_performers.to_string(index=False))
                else:
                    print("No data available for this position.")
            else:
                print("Invalid position. Please enter QB, RB, WR, or TE.")
        
        elif choice == '2':
            week = input("Enter week (e.g., 'Week 1'): ")
            summary = analyzer.create_weekly_summary(week)
            if summary:
                print(f"\n{week} Summary:")
                for position, data in summary.items():
                    print(f"\n{position}s:")
                    print(data.to_string(index=False))
            else:
                print("No data available for this week.")
        
        elif choice == '3':
            position = input("Enter position (QB/RB/WR/TE): ").upper()
            if position in ['QB', 'RB', 'WR', 'TE']:
                consistency = analyzer.get_consistency_analysis(position)
                if not consistency.empty:
                    print(f"\nMost Consistent {position}s:")
                    print(consistency.head(10).to_string(index=False))
                else:
                    print("No consistency data available.")
            else:
                print("Invalid position.")
        
        elif choice == '4':
            position = input("Enter position (QB/RB/WR/TE): ").upper()
            if position in ['QB', 'RB', 'WR', 'TE']:
                breakouts = analyzer.find_breakout_players(position)
                if breakouts is not None and not breakouts.empty:
                    print(f"\n{position} Breakout Players:")
                    print(breakouts.head(5).to_string(index=False))
                else:
                    print("No breakout players found.")
            else:
                print("Invalid position.")
        
        elif choice == '5':
            position = input("Enter position (QB/RB/WR/TE): ").upper()
            if position in ['QB', 'RB', 'WR', 'TE']:
                value_players = analyzer.analyze_value_players(position)
                if value_players is not None and not value_players.empty:
                    print(f"\nBest Value {position}s:")
                    print(value_players.head(5).to_string(index=False))
                else:
                    print("No value analysis available.")
            else:
                print("Invalid position.")
        
        elif choice == '6':
            position = input("Enter position (QB/RB/WR/TE): ").upper()
            if position in ['QB', 'RB', 'WR', 'TE']:
                volatility = analyzer.analyze_weekly_volatility(position)
                if volatility is not None and not volatility.empty:
                    print(f"\nMost Volatile {position}s:")
                    print(volatility.head(5).to_string(index=False))
                else:
                    print("No volatility data available.")
            else:
                print("Invalid position.")
        
        elif choice == '7':
            position = input("Enter position (QB/RB/WR/TE): ").upper()
            if position in ['QB', 'RB', 'WR', 'TE']:
                trends = analyzer.find_emerging_trends(position)
                if trends is not None and not trends.empty:
                    print(f"\n{position}s on the Rise:")
                    print(trends.head(5).to_string(index=False))
                else:
                    print("No emerging trends found.")
            else:
                print("Invalid position.")
        
        elif choice == '8':
            print("Generating comprehensive reports...")
            
            # Generate basic report
            analyzer.generate_report()
            
            # Generate advanced report
            analyzer.generate_advanced_report()
            
            # Generate position dashboards
            for position in analyzer.positions:
                fig = analyzer.create_position_dashboard(position)
                if fig:
                    fig.savefig(f'{position}_dashboard.png', dpi=300, bbox_inches='tight')
            
            # Generate comparison plots
            fig1 = analyzer.plot_position_comparison()
            if fig1:
                fig1.savefig('position_comparison.png', dpi=300, bbox_inches='tight')
            
            print("All reports and visualizations generated!")
            print("Check the following files:")
            print("- fantasy_football_report.html")
            print("- advanced_fantasy_report.html")
            print("- *_dashboard.png files")
            print("- position_comparison.png")
        
        elif choice == '9':
            print("Thanks for using the Fantasy Football Analysis Tool!")
            break
        
        else:
            print("Invalid choice. Please enter a number between 1-9.")

if __name__ == "__main__":
    quick_analysis() 