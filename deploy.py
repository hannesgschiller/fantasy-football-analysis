#!/usr/bin/env python3
"""
Deployment script for Fantasy Football Analysis Dashboard
Helps with GitHub setup and deployment
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_git_status():
    """Check if this is a git repository"""
    if not os.path.exists('.git'):
        print("❌ This is not a git repository")
        print("Initializing git repository...")
        return run_command("git init", "Initializing git repository")
    return True

def setup_git():
    """Setup git repository for deployment"""
    print("🚀 Setting up Git repository for deployment...")
    
    if not check_git_status():
        return False
    
    # Add all files
    if not run_command("git add .", "Adding files to git"):
        return False
    
    # Initial commit
    if not run_command('git commit -m "Initial commit: Fantasy Football Analysis Dashboard"', "Making initial commit"):
        return False
    
    print("\n✅ Git repository setup complete!")
    print("\n📋 Next steps:")
    print("1. Create a new repository on GitHub")
    print("2. Run: git remote add origin https://github.com/yourusername/fantasy-football-analysis.git")
    print("3. Run: git push -u origin main")
    print("4. Deploy to Streamlit Cloud at: https://share.streamlit.io")
    
    return True

def create_sample_data():
    """Create sample data for demonstration"""
    print("📊 Creating sample data for demonstration...")
    
    sample_data = {
        'QB': [
            {'Player': 'Lamar Jackson (BAL)', 'FPTS': 434.4, 'FPTS/G': 25.6},
            {'Player': 'Josh Allen (BUF)', 'FPTS': 385.1, 'FPTS/G': 22.7},
            {'Player': 'Joe Burrow (CIN)', 'FPTS': 381.9, 'FPTS/G': 22.5}
        ],
        'RB': [
            {'Player': 'Saquon Barkley (PHI)', 'FPTS': 322.3, 'FPTS/G': 20.1},
            {'Player': 'Derrick Henry (BAL)', 'FPTS': 317.4, 'FPTS/G': 18.7},
            {'Player': 'Jahmyr Gibbs (DET)', 'FPTS': 310.9, 'FPTS/G': 18.3}
        ],
        'WR': [
            {'Player': 'Ja\'Marr Chase (CIN)', 'FPTS': 276.0, 'FPTS/G': 16.2},
            {'Player': 'Justin Jefferson (MIN)', 'FPTS': 214.5, 'FPTS/G': 12.6},
            {'Player': 'Amon-Ra St. Brown (DET)', 'FPTS': 201.2, 'FPTS/G': 11.8}
        ],
        'TE': [
            {'Player': 'George Kittle (SF)', 'FPTS': 158.6, 'FPTS/G': 10.6},
            {'Player': 'Brock Bowers (LV)', 'FPTS': 150.7, 'FPTS/G': 8.9},
            {'Player': 'Trey McBride (ARI)', 'FPTS': 138.8, 'FPTS/G': 8.7}
        ]
    }
    
    # Create data directory
    os.makedirs('sample_data', exist_ok=True)
    
    import pandas as pd
    
    for position, data in sample_data.items():
        df = pd.DataFrame(data)
        df.to_csv(f'sample_data/{position}_sample.csv', index=False)
    
    print("✅ Sample data created in sample_data/ directory")
    return True

def test_dashboard():
    """Test the dashboard locally"""
    print("🧪 Testing dashboard locally...")
    
    try:
        import streamlit as st
        print("✅ Streamlit is available")
        
        # Test if we can import our modules
        from fantasy_analyzer_simple import FantasyFootballAnalyzer
        print("✅ Analysis modules are working")
        
        print("✅ Dashboard is ready for deployment!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please install requirements: pip install -r requirements.txt")
        return False

def main():
    """Main deployment function"""
    print("🏈 Fantasy Football Analysis Dashboard - Deployment Setup")
    print("=" * 60)
    
    while True:
        print("\nChoose an option:")
        print("1. Setup Git repository for GitHub")
        print("2. Create sample data for demonstration")
        print("3. Test dashboard locally")
        print("4. Run all setup steps")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            setup_git()
        elif choice == '2':
            create_sample_data()
        elif choice == '3':
            test_dashboard()
        elif choice == '4':
            print("\n🔄 Running all setup steps...")
            setup_git()
            create_sample_data()
            test_dashboard()
            print("\n✅ All setup steps completed!")
        elif choice == '5':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter a number between 1-5.")

if __name__ == "__main__":
    main() 