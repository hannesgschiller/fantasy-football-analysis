#!/usr/bin/env python3
"""
Fantasy Football Analysis Launcher
Simple script to run different types of analysis
"""

import os
import sys

def main():
    print("🏈 Fantasy Football Analysis Launcher")
    print("=" * 50)
    print("\nChoose an analysis option:")
    print("1. Basic Analysis (Top performers, consistency, visualizations)")
    print("2. Interactive Quick Analysis")
    print("3. Advanced Analysis (Breakout players, value analysis, trends)")
    print("4. Interactive Dashboard (Streamlit)")
    print("5. View generated reports")
    print("6. Setup for GitHub deployment")
    print("7. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == '1':
            print("\nRunning basic analysis...")
            os.system("python fantasy_analyzer_simple.py")
            print("\nBasic analysis complete!")
            
        elif choice == '2':
            print("\nStarting interactive analysis...")
            os.system("python quick_analysis.py")
            
        elif choice == '3':
            print("\nRunning advanced analysis...")
            try:
                os.system("python advanced_analysis.py")
                print("\nAdvanced analysis complete!")
            except Exception as e:
                print(f"Error running advanced analysis: {e}")
                print("Try running the basic analysis instead.")
            
        elif choice == '4':
            print("\nStarting interactive dashboard...")
            print("The dashboard will open in your web browser.")
            print("If it doesn't open automatically, go to: http://localhost:8501")
            os.system("streamlit run streamlit_app.py")
            
        elif choice == '5':
            print("\nGenerated files:")
            files = [
                "fantasy_football_report.html",
                "advanced_fantasy_report.html",
                "position_comparison.png",
                "QB_dashboard.png",
                "RB_dashboard.png",
                "WR_dashboard.png",
                "TE_dashboard.png"
            ]
            
            for file in files:
                if os.path.exists(file):
                    print(f"✓ {file}")
                else:
                    print(f"✗ {file} (not generated yet)")
            
            print("\nTo view HTML reports, open them in your web browser.")
            print("To view PNG files, open them in any image viewer.")
            
        elif choice == '6':
            print("\nSetting up for GitHub deployment...")
            os.system("python deploy.py")
            
        elif choice == '7':
            print("Thanks for using the Fantasy Football Analysis Tool!")
            break
            
        else:
            print("Invalid choice. Please enter a number between 1-7.")

if __name__ == "__main__":
    main() 