#!/usr/bin/env python3
"""
Streamlit App for Fantasy Football Analysis
Simplified version for deployment with week filtering
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import warnings
from pathlib import Path
import sys
import os

# Add the current directory to path to import our analyzer
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from fantasy_analyzer_simple import FantasyFootballAnalyzer

warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Fantasy Football Analysis",
    page_icon="🏈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Set theme to light mode
st.markdown("""
<style>
    .stApp {
        color-scheme: light;
    }
    .stApp > header {
        background-color: transparent;
    }
    .stApp > div {
        background-color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# Custom CSS for modern design
st.markdown("""
<style>
    /* Modern color scheme */
    :root {
        --primary-color: #1e3a8a;
        --secondary-color: #3b82f6;
        --accent-color: #f59e0b;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --error-color: #ef4444;
        --background-color: #f8fafc;
        --card-background: #ffffff;
        --text-primary: #1f2937;
        --text-secondary: #6b7280;
    }
    
    /* Main header styling */
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Metric cards with modern design */
    .metric-card {
        background: linear-gradient(135deg, #ffffff, #f8fafc);
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        transition: all 0.3s ease;
        margin-bottom: 1rem;
        color: #1f2937;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        border-color: #3b82f6;
    }
    
    /* Week filter styling */
    .week-filter {
        background: #f8fafc;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1.25rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
        color: #374151;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 0.75rem;
        padding-bottom: 0.4rem;
        border-bottom: 2px solid #e5e7eb;
    }
    
    /* Subsection headers */
    .subsection-header {
        font-size: 1.2rem;
        font-weight: 600;
        color: #374151;
        margin-bottom: 0.75rem;
        padding-left: 0.5rem;
        border-left: 3px solid #9ca3af;
    }
    
    /* Info boxes */
    .info-box {
        background: #f9fafb;
        padding: 1rem;
        border-radius: 0.75rem;
        border: 1px solid #e5e7eb;
        margin-bottom: 1rem;
        color: #374151;
    }
    
    /* Warning boxes */
    .warning-box {
        background: #fef3c7;
        padding: 1rem;
        border-radius: 0.75rem;
        border: 1px solid #fbbf24;
        margin-bottom: 1rem;
        color: #92400e;
    }
    
    /* Success boxes */
    .success-box {
        background: #f0fdf4;
        padding: 1rem;
        border-radius: 0.75rem;
        border: 1px solid #86efac;
        margin-bottom: 1rem;
        color: #166534;
    }
    
    /* Chart containers */
    .chart-container {
        background: var(--card-background);
        padding: 1.5rem;
        border-radius: 1rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
    }
    
    /* Data table styling */
    .data-table {
        background: var(--card-background);
        border-radius: 0.75rem;
        overflow: hidden;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, var(--primary-color), var(--secondary-color));
    }
    
    /* Improve sidebar text readability */
    [data-testid="stSidebar"] {
        background-color: #1e293b !important;
    }
    
    [data-testid="stSidebar"] label {
        color: #f1f5f9 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }
    
    [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
        font-weight: 700 !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Specifically target markdown h3 in sidebar */
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3 {
        color: #ffffff !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox label {
        color: #e2e8f0 !important;
    }
    
    [data-testid="stSidebar"] div[data-baseweb="select"] {
        background-color: #334155 !important;
    }
    
    [data-testid="stSidebar"] div[data-baseweb="select"] > div {
        color: #ffffff !important;
        font-weight: 500 !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, var(--secondary-color), var(--primary-color));
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(59, 130, 246, 0.3);
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        border-radius: 0.5rem;
        border: 2px solid #e2e8f0;
    }
    
    /* Slider styling */
    .stSlider > div > div > div > div {
        background: var(--secondary-color);
    }
    
    /* Overall page background */
    .main .block-container {
        background: #ffffff;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Improve text readability */
    .stMarkdown {
        color: #1f2937;
    }
    
    /* Better contrast for labels */
    .stSelectbox label, .stSlider label {
        color: #374151 !important;
        font-weight: 600;
    }
    
    /* Improve metric readability */
    .metric-container {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 0.5rem;
        padding: 1rem;
    }
    
    /* Ensure Streamlit metrics are readable */
    .stMetric {
        background: #ffffff !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 0.5rem !important;
        padding: 1rem !important;
        color: #1f2937 !important;
    }
    
    .stMetric > div > div > div {
        color: #1f2937 !important;
        font-size: 0.9rem !important;
        line-height: 1.2 !important;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
    }
    
    .stMetric label {
        color: #374151 !important;
        font-weight: 600 !important;
        font-size: 0.8rem !important;
    }
    
    .stMetric [data-testid="metric-container"] {
        background: #ffffff !important;
        color: #1f2937 !important;
    }
    
    /* Fix metric value text size and color */
    .stMetric [data-testid="metric-value"] {
        font-size: 0.95rem !important;
        font-weight: 700 !important;
        color: #111827 !important;
        white-space: normal !important;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
        line-height: 1.3 !important;
    }
    
    /* Fix metric label text size and color */
    .stMetric [data-testid="metric-label"] {
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        color: #1f2937 !important;
    }
    
    /* Fix metric delta text size */
    .stMetric [data-testid="metric-delta"] {
        font-size: 0.8rem !important;
    }
    
    /* Force all metric text to be dark and readable */
    .stMetric div {
        color: #111827 !important;
        white-space: normal !important;
    }
    
    /* Specifically target the value display */
    div[data-testid="stMetricValue"] > div {
        color: #111827 !important;
        white-space: normal !important;
        overflow: visible !important;
        text-overflow: clip !important;
    }
    
    /* Allow metric container to expand vertically */
    .stMetric {
        min-height: 80px !important;
    }
    
    /* Ensure tabs are readable */
    .stTabs [data-baseweb="tab-list"] {
        background: #ffffff !important;
        border-bottom: 2px solid #e5e7eb !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #374151 !important;
        font-weight: 600 !important;
    }
    
    .stTabs [aria-selected="true"] {
        color: #1e3a8a !important;
        border-bottom: 2px solid #1e3a8a !important;
    }
    
    /* Make subheaders readable */
    .stApp h3 {
        color: #111827 !important;
        font-weight: 700 !important;
        font-size: 1.3rem !important;
    }
    
    /* Data table header styling */
    .data-header {
        color: #1f2937;
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        padding: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

def load_data():
    """Load fantasy football data without caching to avoid pickle issues"""
    # Try multiple possible data paths for different environments
    possible_paths = [
        "/Users/hannesschiller/Documents/NFL Fantasy data",  # Local development
        "./data/NFL Fantasy data",  # Relative path
        "./NFL Fantasy data",  # Current directory
        "/app/data/NFL Fantasy data",  # Docker/container path
    ]
    
    data_path = None
    for path in possible_paths:
        if os.path.exists(path):
            data_path = path
            break
    
    # If no data path found, use sample data
    if data_path is None:
        st.session_state['using_sample_data'] = True
        return create_sample_data()
    
    try:
        analyzer = FantasyFootballAnalyzer(data_path)
        analyzer.load_weekly_data()
        analyzer.load_season_data()
        st.session_state['using_sample_data'] = False
        st.session_state['data_path'] = data_path
        return analyzer
    except Exception as e:
        st.session_state['using_sample_data'] = True
        st.session_state['load_error'] = str(e)
        return create_sample_data()

def create_sample_data():
    """Create sample data for demonstration with multi-season support"""
    class SampleAnalyzer:
        def __init__(self):
            self.positions = ['QB', 'RB', 'WR', 'TE']
            self.weekly_data = {}
            self.season_data = {}
            self.available_seasons = ['2024', '2025']
            self.is_multi_season = True
            
            # Set random seed for reproducible data
            np.random.seed(42)
            
            # Create sample season data (18-week totals)
            sample_qb = pd.DataFrame({
                'Player': ['Lamar Jackson (BAL)', 'Josh Allen (BUF)', 'Joe Burrow (CIN)', 'Patrick Mahomes (KC)', 'Jalen Hurts (PHI)'],
                'FPTS': [460.8, 408.6, 405.0, 399.6, 397.8],  # 18 weeks * FPTS/G
                'FPTS/G': [25.6, 22.7, 22.5, 22.2, 22.1]
            })
            
            sample_rb = pd.DataFrame({
                'Player': ['Saquon Barkley (PHI)', 'Derrick Henry (BAL)', 'Jahmyr Gibbs (DET)', 'Christian McCaffrey (SF)', 'Alvin Kamara (NO)'],
                'FPTS': [361.8, 336.6, 329.4, 327.6, 322.2],  # 18 weeks * FPTS/G
                'FPTS/G': [20.1, 18.7, 18.3, 18.2, 17.9]
            })
            
            sample_wr = pd.DataFrame({
                'Player': ['Ja\'Marr Chase (CIN)', 'Justin Jefferson (MIN)', 'Amon-Ra St. Brown (DET)', 'Tyreek Hill (MIA)', 'CeeDee Lamb (DAL)'],
                'FPTS': [291.6, 226.8, 212.4, 210.6, 207.0],  # 18 weeks * FPTS/G
                'FPTS/G': [16.2, 12.6, 11.8, 11.7, 11.5]
            })
            
            sample_te = pd.DataFrame({
                'Player': ['George Kittle (SF)', 'Brock Bowers (LV)', 'Trey McBride (ARI)', 'Sam LaPorta (DET)', 'Evan Engram (JAX)'],
                'FPTS': [190.8, 160.2, 156.6, 144.0, 140.4],  # 18 weeks * FPTS/G
                'FPTS/G': [10.6, 8.9, 8.7, 8.0, 7.8]
            })
            
            # Create season data for both 2024 and 2025 with multi-season structure
            self.season_data = {
                '2024': {
                    'QB': sample_qb.copy(),
                    'RB': sample_rb.copy(),
                    'WR': sample_wr.copy(),
                    'TE': sample_te.copy()
                },
                '2025': {
                    'QB': sample_qb.copy(),
                    'RB': sample_rb.copy(),
                    'WR': sample_wr.copy(),
                    'TE': sample_te.copy()
                }
            }
            
            # Create sample weekly data for all 18 weeks with consistent data
            self._create_weekly_data()
        
        def _create_weekly_data(self):
            """Create consistent weekly data - 18 weeks for 2024, 10 weeks for 2025"""
            # Pre-generate weekly variations for consistency
            weekly_variations = {}
            for position in self.positions:
                weekly_variations[position] = []
                for week in range(1, 19):
                    if position == 'QB':
                        variation = np.random.normal(0, 5)
                    elif position == 'RB':
                        variation = np.random.normal(0, 4)
                    elif position == 'WR':
                        variation = np.random.normal(0, 3)
                    else:  # TE
                        variation = np.random.normal(0, 2)
                    weekly_variations[position].append(variation)
            
            # Create weekly data for both seasons with different week counts
            for season in self.available_seasons:
                self.weekly_data[season] = {}
                
                # 2024: Full 18-week season, 2025: Ongoing 10-week season
                max_week = 18 if season == '2024' else 10
                
                # Create weekly data
                for week in range(1, max_week + 1):
                    week_name = f"Week {week}"
                    self.weekly_data[season][week_name] = {}
                    
                    for position in self.positions:
                        if position == 'QB':
                            base_scores = [25.6, 22.7, 22.5, 22.2, 22.1]
                            players = ['Lamar Jackson (BAL)', 'Josh Allen (BUF)', 'Joe Burrow (CIN)', 'Patrick Mahomes (KC)', 'Jalen Hurts (PHI)']
                        elif position == 'RB':
                            base_scores = [20.1, 18.7, 18.3, 18.2, 17.9]
                            players = ['Saquon Barkley (PHI)', 'Derrick Henry (BAL)', 'Jahmyr Gibbs (DET)', 'Christian McCaffrey (SF)', 'Alvin Kamara (NO)']
                        elif position == 'WR':
                            base_scores = [16.2, 12.6, 11.8, 11.7, 11.5]
                            players = ['Ja\'Marr Chase (CIN)', 'Justin Jefferson (MIN)', 'Amon-Ra St. Brown (DET)', 'Tyreek Hill (MIA)', 'CeeDee Lamb (DAL)']
                        else:  # TE
                            base_scores = [10.6, 8.9, 8.7, 8.0, 7.8]
                            players = ['George Kittle (SF)', 'Brock Bowers (LV)', 'Trey McBride (ARI)', 'Sam LaPorta (DET)', 'Evan Engram (JAX)']
                        
                        # Generate weekly scores with consistent variations
                        weekly_variation = weekly_variations[position][week-1]
                        weekly_scores = []
                        
                        for i, base_score in enumerate(base_scores):
                            # Add weekly variation plus individual player variation
                            if position == 'QB':
                                player_variation = np.random.normal(0, 3)
                            elif position == 'RB':
                                player_variation = np.random.normal(0, 2.5)
                            elif position == 'WR':
                                player_variation = np.random.normal(0, 2)
                            else:  # TE
                                player_variation = np.random.normal(0, 1.5)
                            
                            weekly_score = max(0, base_score + weekly_variation + player_variation)
                            weekly_scores.append(round(weekly_score, 1))
                        
                        df = pd.DataFrame({
                            'Player': players,
                            'FPTS': weekly_scores,
                            'FPTS/G': base_scores
                        })
                        
                        self.weekly_data[season][week_name][position] = df
        
        def get_top_performers(self, position, week=None, top_n=10, season=None):
            # Default to most recent season if not specified
            if season is None:
                season = self.available_seasons[-1] if self.available_seasons else '2025'
            
            if week:
                if season in self.weekly_data and week in self.weekly_data[season] and position in self.weekly_data[season][week]:
                    return self.weekly_data[season][week][position].head(top_n)
                return None
            else:
                if season in self.season_data and position in self.season_data[season]:
                    return self.season_data[season][position].head(top_n)
                return None
        
        def get_consistency_analysis(self, position, min_games=3, season=None):
            # Default to most recent season if not specified
            if season is None:
                season = self.available_seasons[-1] if self.available_seasons else '2025'
            
            # Create sample consistency data for full 18-week season
            sample_data = []
            if season in self.season_data and position in self.season_data[season]:
                for i, row in self.season_data[season][position].iterrows():
                    # Generate realistic consistency metrics
                    avg_fpts = row['FPTS/G']
                    std_fpts = avg_fpts * 0.35  # 35% standard deviation for realistic variance
                    min_fpts = max(0, avg_fpts - 2 * std_fpts)  # 2 standard deviations below mean
                    max_fpts = avg_fpts + 2 * std_fpts  # 2 standard deviations above mean
                    
                    # Consistency score: higher score = more consistent
                    consistency_score = avg_fpts / (std_fpts + 1)
                    
                    sample_data.append({
                        'Player': row['Player'],
                        'Games_Played': 18,
                        'Avg_FPTS': round(avg_fpts, 1),
                        'Std_FPTS': round(std_fpts, 1),
                        'Min_FPTS': round(min_fpts, 1),
                        'Max_FPTS': round(max_fpts, 1),
                        'Consistency_Score': round(consistency_score, 2)
                    })
            
            # Sort by consistency score (highest first)
            if sample_data:
                df = pd.DataFrame(sample_data)
                return df.sort_values('Consistency_Score', ascending=False)
            return pd.DataFrame(sample_data)
        
        def debug_weekly_data(self):
            """Debug function to verify weekly data creation"""
            print(f"Total seasons: {len(self.weekly_data)}")
            for season in sorted(self.weekly_data.keys()):
                print(f"\n{season}:")
                print(f"  Total weeks: {len(self.weekly_data[season])}")
                print(f"  Week names: {sorted(self.weekly_data[season].keys())}")
                for week in sorted(self.weekly_data[season].keys()):
                    print(f"  {week}: {list(self.weekly_data[season][week].keys())}")
    
    return SampleAnalyzer()

def format_column_names(df):
    """Format column names to be more readable (remove underscores, proper capitalization)"""
    if df is None or df.empty:
        return df
    
    # Create a copy to avoid modifying the original
    df = df.copy()
    
    # Column name mapping
    column_map = {
        'Total_FPTS': 'Total FPTS',
        'Avg_FPTS': 'Avg FPTS',
        'Games_Played': 'Games Played',
        'Weeks_Played': 'Weeks Played',
        'Std_FPTS': 'Std FPTS',
        'Min_FPTS': 'Min FPTS',
        'Max_FPTS': 'Max FPTS',
        'Consistency_Score': 'Consistency Score',
        'Next_Week_Pred': 'Next Week Pred',
        'Confidence_Low': 'Confidence Low',
        'Confidence_High': 'Confidence High',
        'Current_Avg': 'Current Avg',
        'Current_Total': 'Current Total',
        'Projected_Total': 'Projected Total',
        'Weeks_Remaining': 'Weeks Remaining',
        'Projected_Avg': 'Projected Avg',
        'Projected_Rank': 'Projected Rank',
        'Season_Avg': 'Season Avg',
        'Recent_Avg': 'Recent Avg',
        'Trend_Slope': 'Trend Slope',
        'Momentum_Score': 'Momentum Score',
        'Risk_Score': 'Risk Score',
        'Volatility_Rating': 'Volatility Rating',
        'FPTS/G': 'FPTS per Game'
    }
    
    # Rename columns
    df.rename(columns=column_map, inplace=True)
    
    return df

def get_filtered_data(analyzer, selected_weeks, position, season):
    """Get data filtered by selected weeks and season"""
    if not selected_weeks:
        return None
    
    all_data = []
    
    for week in selected_weeks:
        if season in analyzer.weekly_data and week in analyzer.weekly_data[season] and position in analyzer.weekly_data[season][week]:
            df = analyzer.weekly_data[season][week][position].copy()
            df['Week'] = week
            all_data.append(df)
    
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        
        # Aggregate by player across selected weeks
        player_stats = combined_df.groupby('Player').agg({
            'FPTS': ['sum', 'mean', 'count'],
            'Week': 'count'
        }).reset_index()
        
        # Flatten column names
        player_stats.columns = ['Player', 'Total_FPTS', 'Avg_FPTS', 'Games_Played', 'Weeks_Played']
        
        # Sort by total fantasy points and filter out players with 0 points
        player_stats = player_stats.sort_values('Total_FPTS', ascending=False)
        
        # Filter out players with 0 or negative fantasy points
        player_stats = player_stats[player_stats['Total_FPTS'] > 0]
        
        return player_stats
    
    return None

def create_week_filter(analyzer, selected_season):
    """Create week filter widget"""
    st.markdown('<div class="week-filter">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #1e3a8a; font-weight: 700; margin-bottom: 0.75rem; font-size: 1.1rem;">📅 Week Filter</h3>', unsafe_allow_html=True)
    
    # Get available weeks for the selected season
    if selected_season in analyzer.weekly_data:
        available_weeks = sorted(analyzer.weekly_data[selected_season].keys())
    else:
        available_weeks = []
    
    col1, col2 = st.columns(2)
    
    with col1:
        filter_type = st.selectbox(
            "Filter Type:",
            ["All Weeks", "Single Week", "Week Range", "Custom Selection"]
        )
    
    selected_weeks = []
    
    if filter_type == "All Weeks":
        selected_weeks = available_weeks
        st.markdown(f"""
        <div style="background: #f1f5f9; color: #475569; padding: 0.75rem; border-radius: 0.5rem; border: 1px solid #cbd5e1; font-weight: 500;">
            📊 Showing data for all {len(selected_weeks)} weeks
        </div>
        """, unsafe_allow_html=True)
        
    elif filter_type == "Single Week":
        selected_week = st.selectbox("Select Week:", available_weeks)
        selected_weeks = [selected_week]
        st.markdown(f"""
        <div style="background: #f1f5f9; color: #475569; padding: 0.75rem; border-radius: 0.5rem; border: 1px solid #cbd5e1; font-weight: 500;">
            📊 Showing data for {selected_week}
        </div>
        """, unsafe_allow_html=True)
        
    elif filter_type == "Week Range":
        col1, col2 = st.columns(2)
        with col1:
            start_week = st.selectbox("Start Week:", available_weeks)
        with col2:
            end_week = st.selectbox("End Week:", available_weeks)
        
        start_idx = available_weeks.index(start_week)
        end_idx = available_weeks.index(end_week)
        
        if start_idx <= end_idx:
            selected_weeks = available_weeks[start_idx:end_idx+1]
            st.markdown(f"""
            <div style="background: #f1f5f9; color: #475569; padding: 0.75rem; border-radius: 0.5rem; border: 1px solid #cbd5e1; font-weight: 500;">
                📊 Showing data for weeks {start_week} to {end_week} ({len(selected_weeks)} weeks)
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: #fef2f2; color: #dc2626; padding: 0.75rem; border-radius: 0.5rem; border: 1px solid #ef4444; font-weight: 600;">
                ⚠️ Start week must be before or equal to end week
            </div>
            """, unsafe_allow_html=True)
            
    elif filter_type == "Custom Selection":
        selected_weeks = st.multiselect(
            "Select Weeks:",
            available_weeks,
            default=available_weeks[:5]  # Default to first 5 weeks
        )
        if selected_weeks:
            st.markdown(f"""
            <div style="background: #f1f5f9; color: #475569; padding: 0.75rem; border-radius: 0.5rem; border: 1px solid #cbd5e1; font-weight: 500;">
                📊 Showing data for {len(selected_weeks)} selected weeks
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: #fef3c7; color: #92400e; padding: 0.75rem; border-radius: 0.5rem; border: 1px solid #f59e0b; font-weight: 600;">
                ⚠️ Please select at least one week
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return selected_weeks

def create_top_performers_chart(df, position, title, selected_weeks=None):
    """Create a horizontal bar chart for top performers with modern styling"""
    if df is None or df.empty:
        return go.Figure()
    
    # Limit to top 10 performers
    df = df.head(10)
    
    # Extract player names (remove team info)
    players = [p.split(' (')[0] if ' (' in p else p for p in df['Player']]
    
    # Use Total_FPTS if available (filtered data), otherwise use FPTS
    if 'Total_FPTS' in df.columns:
        values = df['Total_FPTS']
        value_label = "Total Fantasy Points"
    else:
        values = df['FPTS']
        value_label = "Fantasy Points"
    
    # Modern color scheme based on position
    position_colors = {
        'QB': ['#1e3a8a', '#3b82f6', '#60a5fa', '#93c5fd', '#bfdbfe'],
        'RB': ['#059669', '#10b981', '#34d399', '#6ee7b7', '#a7f3d0'],
        'WR': ['#dc2626', '#ef4444', '#f87171', '#fca5a5', '#fecaca'],
        'TE': ['#7c3aed', '#8b5cf6', '#a78bfa', '#c4b5fd', '#ddd6fe']
    }
    
    colors = position_colors.get(position, ['#3b82f6'] * len(values))
    
    fig = go.Figure(data=[
        go.Bar(
            x=values,
            y=players,
            orientation='h',
            marker_color=colors,
            text=[f"{val:.1f}" for val in values],
            textposition='auto',
            textfont=dict(size=12, color='white'),
            marker=dict(
                line=dict(width=1, color='rgba(255,255,255,0.3)')
            )
        )
    ])
    
    # Add week info to title if filtering
    if selected_weeks and len(selected_weeks) < 18:
        if len(selected_weeks) == 1:
            title += f" - {selected_weeks[0]}"
        else:
            title += f" - {len(selected_weeks)} weeks"
    
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=18, color='#1e3a8a'),
            x=0.5
        ),
        xaxis_title=dict(
            text=value_label,
            font=dict(size=14, color='#1f2937')
        ),
        yaxis_title=dict(
            text="Players",
            font=dict(size=14, color='#1f2937')
        ),
        yaxis=dict(
            categoryorder='total ascending',
            tickfont=dict(size=13, color='#111827', family='Arial, sans-serif'),
            tickmode='linear'
        ),
        xaxis=dict(
            tickfont=dict(size=12, color='#1f2937')
        ),
        height=450,
        showlegend=False,
        plot_bgcolor='rgba(255,255,255,1)',
        paper_bgcolor='rgba(255,255,255,1)',
        margin=dict(l=150, r=20, t=60, b=20)
    )
    
    return fig

def create_consistency_chart(consistency_df, position):
    """Create consistency analysis chart with modern styling"""
    if consistency_df.empty:
        return go.Figure()
    
    top_10 = consistency_df.head(10)
    
    # Modern color scheme for consistency
    colors = ['#059669', '#10b981', '#34d399', '#6ee7b7', '#a7f3d0', 
              '#d1fae5', '#ecfdf5', '#f0fdf4', '#f7fee7', '#fefce8']
    
    fig = go.Figure(data=[
        go.Bar(
            x=top_10['Consistency_Score'],
            y=top_10['Player'],
            orientation='h',
            marker_color=colors[:len(top_10)],
            text=[f"{val:.2f}" for val in top_10['Consistency_Score']],
            textposition='auto',
            textfont=dict(size=12, color='white'),
            marker=dict(
                line=dict(width=1, color='rgba(255,255,255,0.3)')
            )
        )
    ])
    
    fig.update_layout(
        title=dict(
            text=f'🎯 Most Consistent {position}s',
            font=dict(size=18, color='#1e3a8a'),
            x=0.5
        ),
        xaxis_title=dict(
            text="Consistency Score (Higher = More Consistent)",
            font=dict(size=14, color='#1f2937')
        ),
        yaxis_title=dict(
            text="Players",
            font=dict(size=14, color='#1f2937')
        ),
        yaxis=dict(
            categoryorder='total ascending',
            tickfont=dict(size=13, color='#111827', family='Arial, sans-serif'),
            tickmode='linear'
        ),
        xaxis=dict(
            tickfont=dict(size=12, color='#1f2937')
        ),
        height=450,
        showlegend=False,
        plot_bgcolor='rgba(255,255,255,1)',
        paper_bgcolor='rgba(255,255,255,1)',
        margin=dict(l=150, r=20, t=60, b=20)
    )
    
    return fig

def create_weekly_trends_chart(analyzer, position, top_n=5, selected_weeks=None, season=None):
    """Create weekly trends chart for top players with modern styling"""
    # Default to most recent season if not specified
    if season is None:
        season = analyzer.available_seasons[-1] if analyzer.available_seasons else '2025'
    
    # Get top players for the season
    season_top = analyzer.get_top_performers(position, week=None, top_n=top_n, season=season)
    if season_top is None:
        return go.Figure()
    
    top_players = [p.split(' (')[0] if ' (' in p else p for p in season_top['Player']]
    
    # Use selected weeks if provided, otherwise use all weeks for the season
    if selected_weeks:
        weeks_to_analyze = selected_weeks
    elif season in analyzer.weekly_data:
        weeks_to_analyze = sorted(analyzer.weekly_data[season].keys())
    else:
        weeks_to_analyze = []
    
    # Track their weekly performance
    weekly_performance = {}
    for player in top_players:
        weekly_performance[player] = []
    
    for week in weeks_to_analyze:
        if season in analyzer.weekly_data and week in analyzer.weekly_data[season] and position in analyzer.weekly_data[season][week]:
            df = analyzer.weekly_data[season][week][position]
            for player in top_players:
                # Find player in this week's data
                player_row = df[df['Player'].str.contains(player, na=False)]
                if not player_row.empty:
                    weekly_performance[player].append(player_row.iloc[0]['FPTS'])
                else:
                    weekly_performance[player].append(0)
    
    # Create the plot with modern styling
    fig = go.Figure()
    
    # Modern color palette for lines
    colors = ['#1e3a8a', '#059669', '#dc2626', '#7c3aed', '#ea580c', 
              '#0891b2', '#be185d', '#65a30d', '#9333ea', '#c2410c']
    
    for i, (player, performance) in enumerate(weekly_performance.items()):
        fig.add_trace(go.Scatter(
            x=list(range(1, len(performance) + 1)),
            y=performance,
            mode='lines+markers',
            name=player,
            line=dict(width=3, color=colors[i % len(colors)]),
            marker=dict(size=6, color=colors[i % len(colors)]),
            hovertemplate=f'<b>{player}</b><br>Week %{{x}}<br>FPTS: %{{y:.1f}}<extra></extra>'
        ))
    
    # Add week info to title if filtering
    title = f'📈 {position} Weekly Performance Trends - Top {top_n} Season Performers'
    if selected_weeks and len(selected_weeks) < 18:
        if len(selected_weeks) == 1:
            title += f" ({selected_weeks[0]})"
        else:
            title += f" ({len(selected_weeks)} weeks)"
    
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=18, color='#1e3a8a'),
            x=0.5
        ),
        xaxis_title=dict(
            text='Week',
            font=dict(size=14, color='#6b7280')
        ),
        yaxis_title=dict(
            text='Fantasy Points',
            font=dict(size=14, color='#6b7280')
        ),
        height=450,
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=60, b=20),
        legend=dict(
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='rgba(0,0,0,0.1)',
            borderwidth=1
        )
    )
    
    return fig

def create_forecast_chart(player_name, forecast_data, historical_data):
    """Create forecast chart showing historical + predicted performance"""
    if historical_data.empty:
        return go.Figure()
    
    fig = go.Figure()
    
    # Historical data
    fig.add_trace(go.Scatter(
        x=historical_data['week'],
        y=historical_data['fpts'],
        mode='lines+markers',
        name='Historical',
        line=dict(color='#1e3a8a', width=3),
        marker=dict(size=8)
    ))
    
    # Forecast point
    if forecast_data:
        next_week = historical_data['week'].max() + 1
        
        fig.add_trace(go.Scatter(
            x=[historical_data['week'].max(), next_week],
            y=[historical_data['fpts'].iloc[-1], forecast_data['predicted_fpts']],
            mode='lines+markers',
            name='Forecast',
            line=dict(color='#f59e0b', width=3, dash='dash'),
            marker=dict(size=10, symbol='star')
        ))
        
        # Confidence interval
        fig.add_trace(go.Scatter(
            x=[next_week, next_week, next_week],
            y=[forecast_data['lower_bound'], forecast_data['predicted_fpts'], forecast_data['upper_bound']],
            mode='markers',
            name='Confidence Range',
            marker=dict(color='#f59e0b', size=12, symbol='line-ns', line=dict(width=3))
        ))
    
    fig.update_layout(
        title=dict(
            text=f'📈 {player_name} - Performance Forecast',
            font=dict(size=18, color='#1e3a8a'),
            x=0.5
        ),
        xaxis_title=dict(
            text='Week',
            font=dict(size=14, color='#1f2937')
        ),
        yaxis_title=dict(
            text='Fantasy Points',
            font=dict(size=14, color='#1f2937')
        ),
        xaxis=dict(
            tickfont=dict(size=12, color='#111827'),
            gridcolor='#e5e7eb'
        ),
        yaxis=dict(
            tickfont=dict(size=12, color='#111827'),
            gridcolor='#e5e7eb'
        ),
        height=400,
        plot_bgcolor='rgba(255,255,255,1)',
        paper_bgcolor='rgba(255,255,255,1)',
        legend=dict(
            bgcolor='rgba(255,255,255,0.95)',
            bordercolor='#9ca3af',
            borderwidth=2,
            font=dict(size=12, color='#111827', family='Arial, sans-serif')
        ),
        hovermode='x unified'
    )
    
    return fig

def create_breakout_chart(breakout_df, position):
    """Create horizontal bar chart for breakout candidates"""
    if breakout_df.empty:
        return go.Figure()
    
    top_10 = breakout_df.head(10)
    players = [p.split(' (')[0] for p in top_10['Player']]
    
    fig = go.Figure(data=[
        go.Bar(
            x=top_10['Momentum_Score'],
            y=players,
            orientation='h',
            marker_color='#10b981',
            text=[f"+{val:.1f}%" for val in top_10['Improvement']],
            textposition='auto',
            textfont=dict(size=12, color='white')
        )
    ])
    
    fig.update_layout(
        title=dict(
            text=f'🚀 Top Breakout Candidates - {position}',
            font=dict(size=18, color='#1e3a8a'),
            x=0.5
        ),
        xaxis_title='Momentum Score',
        yaxis_title='Players',
        yaxis=dict(
            categoryorder='total ascending',
            tickfont=dict(size=13, color='#111827')
        ),
        height=450,
        plot_bgcolor='rgba(255,255,255,1)',
        paper_bgcolor='rgba(255,255,255,1)',
        margin=dict(l=150, r=20, t=60, b=20)
    )
    
    return fig

def create_risk_matrix(risk_data, position):
    """Create scatter plot for risk assessment"""
    if risk_data.empty:
        return go.Figure()
    
    players = [p.split(' (')[0] for p in risk_data['Player']]
    
    # Color by volatility rating
    color_map = {'Low': '#10b981', 'Medium': '#f59e0b', 'High': '#ef4444'}
    colors = [color_map.get(rating, '#6b7280') for rating in risk_data['Volatility_Rating']]
    
    fig = go.Figure(data=[
        go.Scatter(
            x=risk_data['Avg_FPTS'],
            y=risk_data['Volatility'],
            mode='markers+text',
            marker=dict(
                size=12,
                color=colors,
                line=dict(width=1, color='white')
            ),
            text=players,
            textposition='top center',
            textfont=dict(size=9, color='#111827'),
            hovertemplate='<b>%{text}</b><br>Avg: %{x:.1f} FPTS<br>Volatility: %{y:.2f}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title=dict(
            text=f'🎯 Risk/Reward Matrix - {position}',
            font=dict(size=18, color='#1e3a8a'),
            x=0.5
        ),
        xaxis_title='Average Fantasy Points',
        yaxis_title='Volatility (Lower = More Consistent)',
        height=500,
        plot_bgcolor='rgba(255,255,255,1)',
        paper_bgcolor='rgba(255,255,255,1)',
        hovermode='closest'
    )
    
    # Add quadrant lines
    if not risk_data.empty:
        median_fpts = risk_data['Avg_FPTS'].median()
        median_vol = risk_data['Volatility'].median()
        
        fig.add_hline(y=median_vol, line_dash="dash", line_color="#cbd5e1", opacity=0.5)
        fig.add_vline(x=median_fpts, line_dash="dash", line_color="#cbd5e1", opacity=0.5)
    
    return fig

def create_category_distribution(category_df, position):
    """Create pie chart showing player category distribution"""
    if category_df.empty:
        return go.Figure()
    
    category_counts = category_df['Category'].value_counts()
    
    colors = {
        'Elite': '#10b981',
        'Rising Star': '#3b82f6',
        'Consistent': '#8b5cf6',
        'Average': '#6b7280',
        'Volatile': '#f59e0b',
        'Declining': '#ef4444'
    }
    
    fig = go.Figure(data=[
        go.Pie(
            labels=category_counts.index,
            values=category_counts.values,
            marker=dict(colors=[colors.get(cat, '#6b7280') for cat in category_counts.index]),
            textinfo='label+percent',
            textfont=dict(size=12, color='white'),
            hovertemplate='<b>%{label}</b><br>%{value} players<br>%{percent}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title=dict(
            text=f'📊 Player Category Distribution - {position}',
            font=dict(size=18, color='#1e3a8a'),
            x=0.5
        ),
        height=400,
        paper_bgcolor='rgba(255,255,255,1)'
    )
    
    return fig

def main():
    """Main dashboard function"""
    
    # Header with NFL logo - compact professional design
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 1rem; background: linear-gradient(135deg, #f8fafc, #e2e8f0); padding: 0.75rem 1.5rem; border-radius: 0.5rem; margin-bottom: 1.5rem; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1); border: 1px solid #e2e8f0;">
        <img src="https://upload.wikimedia.org/wikipedia/en/a/a2/National_Football_League_logo.svg" 
             alt="NFL Logo" 
             style="width: 50px; height: auto; filter: drop-shadow(0 1px 2px rgba(0,0,0,0.1));">
        <div style="flex: 1;">
            <h1 style="color: #1e293b; font-size: 1.5rem; font-weight: 700; margin: 0; line-height: 1.2;">
                Fantasy Football Analysis Dashboard
            </h1>
            <p style="color: #64748b; font-size: 0.875rem; margin: 0.25rem 0 0 0; font-weight: 400;">
                Professional NFL Analytics & Insights
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data with progress indicator
    with st.spinner('🔄 Loading fantasy football data...'):
        analyzer = load_data()
    
    # Show data source indicator
    if st.session_state.get('using_sample_data', False):
        if 'load_error' in st.session_state:
            st.error(f"⚠️ Error loading real data: {st.session_state['load_error']}")
            st.warning("📊 Using sample/demo data for demonstration. To use your real data, check the error above.")
        else:
            st.info("📊 Using sample/demo data. Real data path not found.")
    else:
        if 'data_path' in st.session_state:
            st.success(f"✅ Loaded real data from: {st.session_state['data_path']}")
    
    # Sidebar for navigation with NFL branding
    st.sidebar.markdown("""
    <div style="text-align: center; margin-bottom: 1rem;">
        <img src="https://upload.wikimedia.org/wikipedia/en/a/a2/National_Football_League_logo.svg" 
             alt="NFL Logo" 
             style="width: 60px; height: auto; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));">
    </div>
    """, unsafe_allow_html=True)
    
    # Season selector in sidebar
    st.sidebar.markdown('<h3 style="text-align: center; color: #ffffff; margin-bottom: 1rem; font-weight: 700;">Season Selection</h3>', unsafe_allow_html=True)
    if hasattr(analyzer, 'available_seasons') and len(analyzer.available_seasons) > 0:
        selected_season = st.sidebar.selectbox(
            "Select Season:",
            analyzer.available_seasons,
            index=len(analyzer.available_seasons) - 1  # Default to most recent
        )
    else:
        selected_season = "2025"  # Default fallback
    
    st.sidebar.markdown("---")
    
    # Week filter
    selected_weeks = create_week_filter(analyzer, selected_season)
    
    st.sidebar.markdown("---")
    
    st.sidebar.markdown('<h3 style="text-align: center; color: #ffffff; margin-bottom: 1rem; font-weight: 700;">Navigation</h3>', unsafe_allow_html=True)
    page = st.sidebar.selectbox(
        "Choose a page:",
        ["Overview", "Position Analysis", "Weekly Trends", "Consistency Analysis", "ML Forecasts", "About"]
    )
    
    if page == "Overview":
        show_overview(analyzer, selected_weeks, selected_season)
    elif page == "Position Analysis":
        show_position_analysis(analyzer, selected_weeks, selected_season)
    elif page == "Weekly Trends":
        show_weekly_trends(analyzer, selected_weeks, selected_season)
    elif page == "Consistency Analysis":
        show_consistency_analysis(analyzer, selected_weeks, selected_season)
    elif page == "ML Forecasts":
        show_ml_forecast(analyzer, selected_weeks, selected_season)
    elif page == "About":
        show_about()

def show_overview(analyzer, selected_weeks, selected_season):
    """Show overview page"""
    st.markdown(f'<h2 class="section-header">📊 {selected_season} Season Overview</h2>', unsafe_allow_html=True)
    
    # Key metrics with modern styling
    st.markdown('<div class="metric-card" style="margin-top: 0.5rem;">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        try:
            if selected_weeks and len(selected_weeks) < 18:
                # Use filtered data for top QB
                qb_data = get_filtered_data(analyzer, selected_weeks, 'QB', selected_season)
                if qb_data is not None and not qb_data.empty:
                    top_qb = qb_data.iloc[0]
                    player_name = top_qb['Player'].split(' (')[0]
                    st.metric("🏈 #1 QB", player_name, f"{top_qb['Total_FPTS']:.1f} pts")
                else:
                    st.metric("🏈 #1 QB", "N/A", "No data")
            else:
                # Use season data
                qb_top = analyzer.get_top_performers('QB', week=None, top_n=1, season=selected_season)
                if qb_top is not None and not qb_top.empty:
                    player_name = qb_top.iloc[0]['Player'].split(' (')[0]
                    st.metric("🏈 #1 QB", player_name, f"{qb_top.iloc[0]['FPTS']:.1f} pts")
                else:
                    st.metric("🏈 #1 QB", "N/A", "No data")
        except Exception as e:
            st.metric("🏈 #1 QB", "Error", str(e)[:20])
    
    with col2:
        try:
            if selected_weeks and len(selected_weeks) < 18:
                rb_data = get_filtered_data(analyzer, selected_weeks, 'RB', selected_season)
                if rb_data is not None and not rb_data.empty:
                    top_rb = rb_data.iloc[0]
                    player_name = top_rb['Player'].split(' (')[0]
                    st.metric("🏃‍♂️ #1 RB", player_name, f"{top_rb['Total_FPTS']:.1f} pts")
                else:
                    st.metric("🏃‍♂️ #1 RB", "N/A", "No data")
            else:
                rb_top = analyzer.get_top_performers('RB', week=None, top_n=1, season=selected_season)
                if rb_top is not None and not rb_top.empty:
                    player_name = rb_top.iloc[0]['Player'].split(' (')[0]
                    st.metric("🏃‍♂️ #1 RB", player_name, f"{rb_top.iloc[0]['FPTS']:.1f} pts")
                else:
                    st.metric("🏃‍♂️ #1 RB", "N/A", "No data")
        except Exception as e:
            st.metric("🏃‍♂️ #1 RB", "Error", str(e)[:20])
    
    with col3:
        try:
            if selected_weeks and len(selected_weeks) < 18:
                wr_data = get_filtered_data(analyzer, selected_weeks, 'WR', selected_season)
                if wr_data is not None and not wr_data.empty:
                    top_wr = wr_data.iloc[0]
                    player_name = top_wr['Player'].split(' (')[0]
                    st.metric("🎯 #1 WR", player_name, f"{top_wr['Total_FPTS']:.1f} pts")
                else:
                    st.metric("🎯 #1 WR", "N/A", "No data")
            else:
                wr_top = analyzer.get_top_performers('WR', week=None, top_n=1, season=selected_season)
                if wr_top is not None and not wr_top.empty:
                    player_name = wr_top.iloc[0]['Player'].split(' (')[0]
                    st.metric("🎯 #1 WR", player_name, f"{wr_top.iloc[0]['FPTS']:.1f} pts")
                else:
                    st.metric("🎯 #1 WR", "N/A", "No data")
        except Exception as e:
            st.metric("🎯 #1 WR", "Error", str(e)[:20])
    
    with col4:
        try:
            if selected_weeks and len(selected_weeks) < 18:
                te_data = get_filtered_data(analyzer, selected_weeks, 'TE', selected_season)
                if te_data is not None and not te_data.empty:
                    top_te = te_data.iloc[0]
                    player_name = top_te['Player'].split(' (')[0]
                    st.metric("🎪 #1 TE", player_name, f"{top_te['Total_FPTS']:.1f} pts")
                else:
                    st.metric("🎪 #1 TE", "N/A", "No data")
            else:
                te_top = analyzer.get_top_performers('TE', week=None, top_n=1, season=selected_season)
                if te_top is not None and not te_top.empty:
                    player_name = te_top.iloc[0]['Player'].split(' (')[0]
                    st.metric("🎪 #1 TE", player_name, f"{te_top.iloc[0]['FPTS']:.1f} pts")
                else:
                    st.metric("🎪 #1 TE", "N/A", "No data")
        except Exception as e:
            st.metric("🎪 #1 TE", "Error", str(e)[:20])
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Top performers by position
    st.markdown('<h3 class="subsection-header">🏆 Top Performers by Position</h3>', unsafe_allow_html=True)
    
    tabs = st.tabs(["QB", "RB", "WR", "TE"])
    
    for i, position in enumerate(['QB', 'RB', 'WR', 'TE']):
        with tabs[i]:
            if selected_weeks and len(selected_weeks) < 18:
                # Use filtered data
                position_data = get_filtered_data(analyzer, selected_weeks, position, selected_season)
                if position_data is not None:
                    fig = create_top_performers_chart(position_data, position, f"Top 10 {position}s", selected_weeks)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Show data table
                    st.markdown(f'<div class="data-header">📊 Top 10 {position}s Data</div>', unsafe_allow_html=True)
                    st.dataframe(format_column_names(position_data.head(10)), use_container_width=True)
            else:
                # Use season data
                top_performers = analyzer.get_top_performers(position, week=None, top_n=10, season=selected_season)
                if top_performers is not None:
                    fig = create_top_performers_chart(top_performers, position, f"Top 10 {position}s")
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Show data table
                    st.markdown(f'<div class="data-header">📊 Top 10 {position}s Data</div>', unsafe_allow_html=True)
                    st.dataframe(format_column_names(top_performers), use_container_width=True)

def show_position_analysis(analyzer, selected_weeks, selected_season):
    """Show position-specific analysis"""
    st.markdown(f'<h2 class="section-header">🎯 {selected_season} Position Analysis</h2>', unsafe_allow_html=True)
    
    position = st.selectbox("Select Position:", ['QB', 'RB', 'WR', 'TE'])
    
    # Top performers
    st.markdown(f'<h3 class="subsection-header">🏆 Top 10 {position}s</h3>', unsafe_allow_html=True)
    
    if selected_weeks and len(selected_weeks) < 18:
        # Use filtered data
        position_data = get_filtered_data(analyzer, selected_weeks, position, selected_season)
        if position_data is not None:
            fig = create_top_performers_chart(position_data, position, f"Top 10 {position}s", selected_weeks)
            st.plotly_chart(fig, use_container_width=True)
            
            # Show data table
            st.dataframe(format_column_names(position_data.head(10)), use_container_width=True)
    else:
        # Use season data
        top_performers = analyzer.get_top_performers(position, week=None, top_n=10, season=selected_season)
        if top_performers is not None:
            fig = create_top_performers_chart(top_performers, position, f"Top 10 {position}s")
            st.plotly_chart(fig, use_container_width=True)
            
            # Show data table
            st.dataframe(format_column_names(top_performers), use_container_width=True)

def show_weekly_trends(analyzer, selected_weeks, selected_season):
    """Show weekly trends analysis"""
    st.markdown(f'<h2 class="section-header">📈 {selected_season} Weekly Trends</h2>', unsafe_allow_html=True)
    
    position = st.selectbox("Select Position:", ['QB', 'RB', 'WR', 'TE'])
    top_n = st.slider("Number of top players to show:", 3, 10, 5)
    
    # Weekly trends chart
    fig = create_weekly_trends_chart(analyzer, position, top_n, selected_weeks, selected_season)
    st.plotly_chart(fig, use_container_width=True)
    
    # Weekly summary
    if selected_weeks and len(selected_weeks) < 18:
        st.markdown(f'<div class="data-header">📅 Weekly Summary ({len(selected_weeks)} weeks)</div>', unsafe_allow_html=True)
        for week in selected_weeks:
            if selected_season in analyzer.weekly_data and week in analyzer.weekly_data[selected_season] and position in analyzer.weekly_data[selected_season][week]:
                df = analyzer.weekly_data[selected_season][week][position]
                top_3 = df.nlargest(3, 'FPTS')[['Player', 'FPTS']]
                st.write(f"**{week} - Top 3 {position}s:**")
                st.dataframe(top_3, use_container_width=True)

def show_consistency_analysis(analyzer, selected_weeks, selected_season):
    """Show consistency analysis"""
    st.markdown(f'<h2 class="section-header">🎯 {selected_season} Consistency Analysis</h2>', unsafe_allow_html=True)
    
    position = st.selectbox("Select Position:", ['QB', 'RB', 'WR', 'TE'])
    min_games = st.slider("Minimum games played:", 3, 10, 5)
    
    # Note: Consistency analysis works best with full season data
    # For filtered weeks, we'll show a note
    if selected_weeks and len(selected_weeks) < 18:
        st.markdown(f"""
        <div class="warning-box">
            <strong style="color: #92400e;">📝 Note:</strong> 
            <span style="color: #1f2937;">Consistency analysis is shown for the full season. You're currently filtering {len(selected_weeks)} weeks.</span>
        </div>
        """, unsafe_allow_html=True)
    
    consistency = analyzer.get_consistency_analysis(position, min_games=min_games, season=selected_season)
    
    if not consistency.empty:
        # Consistency chart
        fig = create_consistency_chart(consistency, position)
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed consistency data
        st.markdown('<div class="data-header">📊 Detailed Consistency Analysis</div>', unsafe_allow_html=True)
        st.dataframe(format_column_names(consistency), use_container_width=True)
        
        # Consistency insights
        st.markdown('<div class="data-header">💡 Key Insights</div>', unsafe_allow_html=True)
        most_consistent = consistency.iloc[0]
        least_consistent = consistency.iloc[-1]
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**Most Consistent:** {most_consistent['Player']}")
            st.write(f"Average: {most_consistent['Avg_FPTS']:.1f} FPTS")
            st.write(f"Consistency Score: {most_consistent['Consistency_Score']:.2f}")
        
        with col2:
            st.warning(f"**Least Consistent:** {least_consistent['Player']}")
            st.write(f"Average: {least_consistent['Avg_FPTS']:.1f} FPTS")
            st.write(f"Consistency Score: {least_consistent['Consistency_Score']:.2f}")

def show_ml_forecast(analyzer, selected_weeks, selected_season):
    """Show ML forecasting and predictions page"""
    st.markdown(f'<h2 class="section-header">🤖 {selected_season} ML Forecasts & Predictions</h2>', unsafe_allow_html=True)
    
    # Import ML forecaster
    try:
        from fantasy_ml_forecaster import FantasyMLForecaster
        forecaster = FantasyMLForecaster(analyzer, selected_season)
    except Exception as e:
        st.error(f"Error loading ML forecaster: {str(e)}")
        st.info("ML forecasting features require additional packages. Install with: pip install -r requirements.txt")
        return
    
    # Data availability check
    if selected_season not in analyzer.weekly_data or not analyzer.weekly_data[selected_season]:
        st.warning(f"No weekly data available for {selected_season} season. ML forecasts require historical weekly data.")
        st.info("Please ensure you have weekly data loaded for the selected season.")
        return
    
    weeks_available = len(analyzer.weekly_data[selected_season])
    if weeks_available < 3:
        st.warning(f"Only {weeks_available} weeks of data available. ML forecasts require at least 3 weeks of historical data for meaningful predictions.")
        return
    
    # Show data info
    st.info(f"📊 Analyzing {weeks_available} weeks of {selected_season} season data for ML predictions")
    
    # Position selector
    position = st.selectbox("Select Position:", ['QB', 'RB', 'WR', 'TE'], key='ml_position')
    
    # Create tabs for different ML analyses
    tabs = st.tabs(["Next Week Predictions", "Season Projections", "Breakout & Bust Analysis", "Risk Assessment"])
    
    # Tab 1: Next Week Predictions
    with tabs[0]:
        st.markdown('<h3 class="subsection-header">🔮 Next Week Predictions</h3>', unsafe_allow_html=True)
        
        with st.spinner('Generating forecasts...'):
            try:
                forecasts_df = forecaster.get_all_player_forecasts(position, top_n=10)
                    
            except Exception as e:
                st.error(f"❌ Error generating forecasts: {str(e)}")
                import traceback
                st.code(traceback.format_exc())
                forecasts_df = pd.DataFrame()
        
        if forecasts_df is not None and not forecasts_df.empty:
            st.markdown('<div class="data-header">📊 Top 10 Predicted Performers for Next Week</div>', unsafe_allow_html=True)
            st.dataframe(format_column_names(forecasts_df), use_container_width=True)
            
            # Player selector for detailed forecast
            st.markdown("---")
            st.markdown('<div class="data-header">📈 Detailed Player Forecast</div>', unsafe_allow_html=True)
            
            players = [p.split(' (')[0] for p in forecasts_df['Player']]
            selected_player = st.selectbox("Select player for detailed forecast:", players, key='forecast_player')
            
            if selected_player:
                # Get player data
                from fantasy_ml_forecaster import FantasyMLForecaster
                forecaster_detail = FantasyMLForecaster(analyzer, selected_season)
                historical_data = forecaster_detail.prepare_player_data(selected_player, position)
                forecast_data = forecaster_detail.forecast_next_week(selected_player, position)
                
                if not historical_data.empty and forecast_data:
                    # Show forecast chart
                    fig = create_forecast_chart(selected_player, forecast_data, historical_data)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Show forecast details
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Predicted FPTS", f"{forecast_data['predicted_fpts']:.1f}")
                    with col2:
                        st.metric("Lower Bound", f"{forecast_data['lower_bound']:.1f}")
                    with col3:
                        st.metric("Upper Bound", f"{forecast_data['upper_bound']:.1f}")
        else:
            st.info("No forecasts generated. This could be due to insufficient weekly data for individual players.")
    
    # Tab 2: Season Projections
    with tabs[1]:
        st.markdown('<h3 class="subsection-header">📅 Season-End Projections</h3>', unsafe_allow_html=True)
        
        projections = []
        
        try:
            # Try season data first
            top_players = analyzer.get_top_performers(position, week=None, top_n=15, season=selected_season)
            
            # If no season data, use weekly data fallback
            if top_players is None or top_players.empty:
                top_players = forecaster._get_top_from_weekly(position, top_n=15)
                
        except Exception as e:
            st.error(f"Error getting top performers: {str(e)}")
            import traceback
            st.code(traceback.format_exc())
            top_players = None
        
        if top_players is not None and not top_players.empty:
            with st.spinner('Calculating projections...'):
                for _, row in top_players.iterrows():
                    player_name = row['Player'].split(' (')[0]
                    projection = forecaster.forecast_season_end(player_name, position)
                    
                    if projection:
                        projections.append({
                            'Player': row['Player'],
                            'Current_Total': projection['current_total'],
                            'Projected_Total': projection['projected_total'],
                            'Weeks_Remaining': projection['weeks_remaining'],
                            'Projected_Avg': projection['avg_per_week']
                        })
            
            if projections:
                proj_df = pd.DataFrame(projections)
                proj_df = proj_df.sort_values('Projected_Total', ascending=False)
                proj_df['Projected_Rank'] = range(1, len(proj_df) + 1)
                
                st.markdown('<div class="data-header">📊 Projected Season-End Rankings</div>', unsafe_allow_html=True)
                st.dataframe(format_column_names(proj_df), use_container_width=True)
                
                # Show projection chart
                fig = go.Figure()
                players = [p.split(' (')[0] for p in proj_df['Player'].head(10)]
                
                fig.add_trace(go.Bar(
                    name='Current Total',
                    x=players,
                    y=proj_df['Current_Total'].head(10),
                    marker_color='#3b82f6'
                ))
                
                fig.add_trace(go.Bar(
                    name='Projected Additional',
                    x=players,
                    y=(proj_df['Projected_Total'] - proj_df['Current_Total']).head(10),
                    marker_color='#10b981'
                ))
                
                fig.update_layout(
                    title=f'Season-End Projections - Top 10 {position}s',
                    xaxis_title='Players',
                    yaxis_title='Fantasy Points',
                    barmode='stack',
                    height=450,
                    plot_bgcolor='rgba(255,255,255,1)',
                    paper_bgcolor='rgba(255,255,255,1)'
                )
                
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(f"No projection data available for {position}s.")
    
    # Tab 3: Breakout & Bust Analysis
    with tabs[2]:
        st.markdown('<h3 class="subsection-header">🚀 Breakout & Bust Analysis</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="data-header">🚀 Breakout Candidates</div>', unsafe_allow_html=True)
            with st.spinner('Identifying breakouts...'):
                try:
                    breakouts = forecaster.identify_breakout_players(position, threshold=0.10, min_weeks=3)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    breakouts = pd.DataFrame()
            
            if not breakouts.empty:
                st.dataframe(format_column_names(breakouts.head(10)), use_container_width=True)
                fig = create_breakout_chart(breakouts, position)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No significant breakout candidates identified (threshold: >10% improvement).")
        
        with col2:
            st.markdown('<div class="data-header">⚠️ Bust Risks</div>', unsafe_allow_html=True)
            with st.spinner('Identifying bust risks...'):
                try:
                    busts = forecaster.identify_bust_risks(position, threshold=-0.10, min_weeks=3)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    busts = pd.DataFrame()
            
            if not busts.empty:
                st.dataframe(format_column_names(busts.head(10)), use_container_width=True)
                
                # Bust risk chart
                top_10 = busts.head(10)
                players = [p.split(' (')[0] for p in top_10['Player']]
                
                fig = go.Figure(data=[
                    go.Bar(
                        x=top_10['Risk_Score'],
                        y=players,
                        orientation='h',
                        marker_color='#ef4444',
                        text=[f"{val:.1f}%" for val in top_10['Decline']],
                        textposition='auto',
                        textfont=dict(size=12, color='white')
                    )
                ])
                
                fig.update_layout(
                    title=f'⚠️ High Bust Risk - {position}',
                    xaxis_title='Risk Score',
                    yaxis_title='Players',
                    yaxis=dict(
                        categoryorder='total ascending',
                        tickfont=dict(size=13, color='#111827')
                    ),
                    height=450,
                    plot_bgcolor='rgba(255,255,255,1)',
                    paper_bgcolor='rgba(255,255,255,1)',
                    margin=dict(l=150, r=20, t=60, b=20)
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No significant bust risks identified (threshold: >10% decline).")
    
    # Tab 4: Risk Assessment
    with tabs[3]:
        st.markdown('<h3 class="subsection-header">🎯 Risk Assessment & Player Categories</h3>', unsafe_allow_html=True)
        
        with st.spinner('Analyzing player categories...'):
            try:
                categories = forecaster.predict_player_category(position)
                risk_assessment = forecaster.get_risk_assessment(position)
            except Exception as e:
                st.error(f"Error: {str(e)}")
                categories = pd.DataFrame()
                risk_assessment = pd.DataFrame()
        
        if not categories.empty:
            # Category distribution
            col1, col2 = st.columns([1, 1])
            
            with col1:
                fig = create_category_distribution(categories, position)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown('<div class="data-header">📋 Player Categories</div>', unsafe_allow_html=True)
                st.dataframe(format_column_names(categories), use_container_width=True)
            
            # Risk matrix
            if not risk_assessment.empty:
                st.markdown("---")
                st.markdown('<div class="data-header">🎯 Risk/Reward Matrix</div>', unsafe_allow_html=True)
                fig = create_risk_matrix(risk_assessment, position)
                st.plotly_chart(fig, use_container_width=True)
                
                # Legend explanation
                st.markdown("""
                <div style="background: #f9fafb; padding: 1rem; border-radius: 0.5rem; border: 1px solid #e5e7eb; margin-top: 1rem;">
                    <h4 style="color: #374151; margin-bottom: 0.5rem; font-size: 0.95rem;">📊 Risk Matrix Guide:</h4>
                    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.5rem; font-size: 0.85rem;">
                        <div><span style="color: #10b981;">●</span> <strong>Low Volatility:</strong> Consistent performers</div>
                        <div><span style="color: #f59e0b;">●</span> <strong>Medium Volatility:</strong> Moderate risk</div>
                        <div><span style="color: #ef4444;">●</span> <strong>High Volatility:</strong> Boom/bust players</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info(f"Insufficient data for ML analysis of {position}s.")

def show_about():
    """Show about page"""
    st.markdown('<h2 class="section-header">ℹ️ About This Dashboard</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="metric-card">
        <div style="text-align: center; margin-bottom: 1rem;">
            <img src="https://upload.wikimedia.org/wikipedia/en/a/a2/National_Football_League_logo.svg" 
                 alt="NFL Logo" 
                 style="width: 80px; height: auto; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1)); margin-bottom: 0.5rem;">
        </div>
        <h3 style="color: #374151; margin-bottom: 1rem; text-align: center;">🏈 Fantasy Football Analysis Dashboard</h3>
        
        <p style="font-size: 1.1rem; color: #374151; margin-bottom: 1.5rem;">
            This interactive dashboard provides comprehensive analysis of fantasy football data from FantasyPros.
        </p>
        
        <h4 style="color: #475569; margin-bottom: 0.5rem;">✨ Features:</h4>
        <ul style="color: #6b7280; margin-bottom: 1.5rem;">
            <li><strong>Season Overview:</strong> Top performers and position comparisons</li>
            <li><strong>Position Analysis:</strong> Detailed analysis for each position (QB, RB, WR, TE)</li>
            <li><strong>Weekly Trends:</strong> Track player performance over time</li>
            <li><strong>Consistency Analysis:</strong> Identify reliable players</li>
            <li><strong>Week Filtering:</strong> Analyze specific weeks or week ranges</li>
        </ul>
        
        <h4 style="color: #475569; margin-bottom: 0.5rem;">🛠️ Technology:</h4>
        <ul style="color: #6b7280; margin-bottom: 1.5rem;">
            <li>Built with <strong>Streamlit</strong></li>
            <li>Interactive <strong>Plotly</strong> charts</li>
            <li>Real-time data analysis</li>
            <li>Advanced filtering capabilities</li>
        </ul>
        
        <h4 style="color: #475569; margin-bottom: 0.5rem;">🚀 Deployment:</h4>
        <p style="color: #6b7280; margin-bottom: 1.5rem;">
            This dashboard is designed to be deployed on Streamlit Cloud or any web hosting service.
        </p>
        
        <h4 style="color: #475569; margin-bottom: 0.5rem;">👨‍💻 Author:</h4>
        <p style="color: #6b7280;">
            Professional fantasy football analysis tool for data-driven decision making.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    <div class="info-box">
        <strong>🔗 GitHub Repository:</strong> <a href="https://github.com/hannesgschiller/fantasy-football-analysis" target="_blank">fantasy-football-analysis</a><br>
        <strong>📧 Contact:</strong> [Add your contact information here]
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 