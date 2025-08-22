#!/usr/bin/env python3
"""
Script to reload fantasy football data with fixes
"""

import streamlit as st
import os
import sys
from pathlib import Path

# Add the current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from fantasy_analyzer_simple import FantasyFootballAnalyzer

def clear_cache_and_reload():
    """Clear Streamlit cache and reload data"""
    print("🔄 Clearing cache and reloading data...")
    
    # Clear Streamlit cache
    try:
        st.cache_data.clear()
        print("✅ Streamlit cache cleared")
    except:
        print("⚠️ Could not clear Streamlit cache (this is normal if not running in Streamlit)")
    
    # Test data loading
    data_path = "/Users/hannesschiller/Documents/NFL Fantasy data"
    
    if not os.path.exists(data_path):
        print(f"❌ Data path not found: {data_path}")
        return False
    
    print(f"✅ Data path found: {data_path}")
    
    # Load data
    try:
        analyzer = FantasyFootballAnalyzer(data_path)
        analyzer.load_weekly_data()
        analyzer.load_season_data()
        
        print(f"✅ Successfully loaded data for {len(analyzer.weekly_data)} weeks")
        print(f"✅ Successfully loaded season data for {len(analyzer.season_data)} positions")
        
        # Test getting some data
        for position in ['QB', 'RB', 'WR', 'TE']:
            if position in analyzer.season_data:
                top_player = analyzer.get_top_performers(position, week=None, top_n=1)
                if top_player is not None:
                    print(f"✅ {position} data loaded - Top player: {top_player.iloc[0]['Player']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return False

def main():
    """Main function"""
    print("🏈 Fantasy Football Data Reload")
    print("=" * 40)
    
    success = clear_cache_and_reload()
    
    if success:
        print("\n🎉 Data reload successful!")
        print("\n📋 Next steps:")
        print("1. Run: streamlit run streamlit_app.py")
        print("2. Your dashboard will now use the updated data")
        print("3. Test the week filtering with your corrected data")
    else:
        print("\n❌ Data reload failed. Please check your data files.")

if __name__ == "__main__":
    main() 