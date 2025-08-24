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
        padding: 1.5rem;
        border-radius: 1rem;
        border: 2px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
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
        padding: 1.5rem;
        border-radius: 1rem;
        margin-bottom: 1.5rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        color: #374151;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.8rem;
        font-weight: 700;
        color: #374151;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #d1d5db;
    }
    
    /* Subsection headers */
    .subsection-header {
        font-size: 1.4rem;
        font-weight: 600;
        color: #4b5563;
        margin-bottom: 1rem;
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
    }
    
    .stMetric label {
        color: #374151 !important;
        font-weight: 600 !important;
    }
    
    .stMetric [data-testid="metric-container"] {
        background: #ffffff !important;
        color: #1f2937 !important;
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
        st.markdown("""
        <div class="info-box">
            <strong style="color: #475569;">📊 Using sample data for demonstration.</strong> 
            <span style="color: #64748b;">To use real data, add your fantasy football data files to the project.</span>
        </div>
        """, unsafe_allow_html=True)
        return create_sample_data()
    
    try:
        analyzer = FantasyFootballAnalyzer(data_path)
        analyzer.load_weekly_data()
        analyzer.load_season_data()
        st.markdown(f"""
        <div class="success-box">
            <strong style="color: #166534;">✅ Loaded data from:</strong> 
            <span style="color: #374151;">{data_path}</span>
        </div>
        """, unsafe_allow_html=True)
        return analyzer
    except Exception as e:
        st.markdown(f"""
        <div class="warning-box">
            <strong style="color: #92400e;">⚠️ Error loading data from {data_path}:</strong> 
            <span style="color: #1f2937;">{str(e)}</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="info-box">
            <strong style="color: #065f46;">📊 Falling back to sample data for demonstration.</strong>
        </div>
        """, unsafe_allow_html=True)
        return create_sample_data()

def create_sample_data():
    """Create sample data for demonstration"""
    class SampleAnalyzer:
        def __init__(self):
            self.positions = ['QB', 'RB', 'WR', 'TE']
            self.weekly_data = {}
            self.season_data = {}
            
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
            
            self.season_data = {
                'QB': sample_qb,
                'RB': sample_rb,
                'WR': sample_wr,
                'TE': sample_te
            }
            
            # Create sample weekly data for all 18 weeks with consistent data
            self._create_weekly_data()
        
        def _create_weekly_data(self):
            """Create consistent weekly data for all 18 weeks"""
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
            
            # Create weekly data for all 18 weeks
            for week in range(1, 19):
                week_name = f"Week {week}"
                self.weekly_data[week_name] = {}
                
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
                    
                    self.weekly_data[week_name][position] = df
        
        def get_top_performers(self, position, week=None, top_n=10):
            if week:
                if week in self.weekly_data and position in self.weekly_data[week]:
                    return self.weekly_data[week][position].head(top_n)
                return None
            else:
                if position in self.season_data:
                    return self.season_data[position].head(top_n)
                return None
        
        def get_consistency_analysis(self, position, min_games=3):
            # Create sample consistency data for full 18-week season
            sample_data = []
            if position in self.season_data:
                for i, row in self.season_data[position].iterrows():
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
            print(f"Total weeks created: {len(self.weekly_data)}")
            print(f"Week names: {sorted(self.weekly_data.keys())}")
            for week in sorted(self.weekly_data.keys()):
                print(f"{week}: {list(self.weekly_data[week].keys())}")
    
    return SampleAnalyzer()

def get_filtered_data(analyzer, selected_weeks, position):
    """Get data filtered by selected weeks"""
    if not selected_weeks:
        return None
    
    all_data = []
    
    for week in selected_weeks:
        if week in analyzer.weekly_data and position in analyzer.weekly_data[week]:
            df = analyzer.weekly_data[week][position].copy()
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

def create_week_filter():
    """Create week filter widget"""
    st.markdown('<div class="week-filter">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #1e3a8a; font-weight: 700; margin-bottom: 1rem;">📅 Week Filter</h3>', unsafe_allow_html=True)
    
    # Get available weeks
    analyzer = load_data()
    available_weeks = sorted(analyzer.weekly_data.keys())
    
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
            font=dict(size=14, color='#6b7280')
        ),
        yaxis_title=dict(
            text="Players",
            font=dict(size=14, color='#6b7280')
        ),
        height=450,
        showlegend=False,
        yaxis={'categoryorder': 'total ascending'},
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=60, b=20)
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
            font=dict(size=14, color='#6b7280')
        ),
        yaxis_title=dict(
            text="Players",
            font=dict(size=14, color='#6b7280')
        ),
        height=450,
        showlegend=False,
        yaxis={'categoryorder': 'total ascending'},
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    return fig

def create_weekly_trends_chart(analyzer, position, top_n=5, selected_weeks=None):
    """Create weekly trends chart for top players with modern styling"""
    # Get top players for the season
    season_top = analyzer.get_top_performers(position, week=None, top_n=top_n)
    if season_top is None:
        return go.Figure()
    
    top_players = [p.split(' (')[0] if ' (' in p else p for p in season_top['Player']]
    
    # Use selected weeks if provided, otherwise use all weeks
    weeks_to_analyze = selected_weeks if selected_weeks else sorted(analyzer.weekly_data.keys())
    
    # Track their weekly performance
    weekly_performance = {}
    for player in top_players:
        weekly_performance[player] = []
    
    for week in weeks_to_analyze:
        if position in analyzer.weekly_data[week]:
            df = analyzer.weekly_data[week][position]
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

def main():
    """Main dashboard function"""
    
    # Header with NFL logo and modern styling
    st.markdown("""
    <div style="text-align: center; background: linear-gradient(135deg, #1e3a8a, #3b82f6); padding: 2rem; border-radius: 1rem; margin-bottom: 2rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
        <img src="https://upload.wikimedia.org/wikipedia/en/a/a2/National_Football_League_logo.svg" 
             alt="NFL Logo" 
             style="width: 120px; height: auto; filter: drop-shadow(0 4px 8px rgba(0,0,0,0.2)); margin-bottom: 1rem;">
        <h1 style="color: white; font-size: 2.5rem; font-weight: 800; margin: 0; text-shadow: 0 2px 4px rgba(0,0,0,0.3);">
            🏈 Fantasy Football Analysis Dashboard
        </h1>
        <p style="color: white; font-size: 1.1rem; margin: 0.5rem 0 0 0; font-weight: 500;">
            Professional NFL Fantasy Football Analytics & Insights
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data with progress indicator
    with st.spinner('🔄 Loading fantasy football data...'):
        analyzer = load_data()
    
    # Debug: Show available weeks with modern styling
    if hasattr(analyzer, 'weekly_data'):
        available_weeks = sorted(analyzer.weekly_data.keys())
        st.markdown(f"""
        <div class="info-box">
            <strong style="color: #065f46;">📊 Data Overview:</strong> 
            <span style="color: #1f2937;">{len(available_weeks)} weeks available - {', '.join(available_weeks[:5])}{'...' if len(available_weeks) > 5 else ''}</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="success-box"><strong style="color: #065f46;">✅ Data loaded successfully!</strong></div>', unsafe_allow_html=True)
    
    # Week filter
    selected_weeks = create_week_filter()
    
    # Sidebar for navigation with NFL branding
    st.sidebar.markdown("""
    <div style="text-align: center; margin-bottom: 1rem;">
        <img src="https://upload.wikimedia.org/wikipedia/en/a/a2/National_Football_League_logo.svg" 
             alt="NFL Logo" 
             style="width: 60px; height: auto; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));">
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown('<h3 style="text-align: center; color: #1e3a8a; margin-bottom: 1rem;">Navigation</h3>', unsafe_allow_html=True)
    page = st.sidebar.selectbox(
        "Choose a page:",
        ["Overview", "Position Analysis", "Weekly Trends", "Consistency Analysis", "About"]
    )
    
    if page == "Overview":
        show_overview(analyzer, selected_weeks)
    elif page == "Position Analysis":
        show_position_analysis(analyzer, selected_weeks)
    elif page == "Weekly Trends":
        show_weekly_trends(analyzer, selected_weeks)
    elif page == "Consistency Analysis":
        show_consistency_analysis(analyzer, selected_weeks)
    elif page == "About":
        show_about()

def show_overview(analyzer, selected_weeks):
    """Show overview page"""
    st.markdown('<h2 class="section-header">📊 Season Overview</h2>', unsafe_allow_html=True)
    
    # Debug: Show what data we have
    try:
        selected_weeks_count = len(selected_weeks) if selected_weeks else 0
        season_data_count = len(analyzer.season_data) if hasattr(analyzer, 'season_data') and analyzer.season_data else 0
        
        st.markdown(f"""
        <div style="background: #f8fafc; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem; border: 1px solid #e2e8f0;">
            <strong style="color: #475569;">🔍 Debug Info:</strong> 
            <span style="color: #64748b;">Selected weeks: {selected_weeks_count} | 
            Season data available: {season_data_count} positions</span>
        </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.markdown(f"""
        <div style="background: #fef2f2; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem; border: 1px solid #ef4444;">
            <strong style="color: #dc2626;">⚠️ Debug Error:</strong> 
            <span style="color: #6b7280;">{str(e)[:50]}</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Key metrics with modern styling
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        try:
            if selected_weeks and len(selected_weeks) < 18:
                # Use filtered data for top QB
                qb_data = get_filtered_data(analyzer, selected_weeks, 'QB')
                if qb_data is not None and not qb_data.empty:
                    top_qb = qb_data.iloc[0]
                    st.metric("🏈 Top QB", f"{top_qb['Player'].split(' (')[0]}", f"{top_qb['Total_FPTS']:.1f} pts")
                else:
                    st.metric("🏈 Top QB", "N/A", "No data")
            else:
                # Use season data
                qb_top = analyzer.get_top_performers('QB', week=None, top_n=1)
                if qb_top is not None and not qb_top.empty:
                    st.metric("🏈 Top QB", f"{qb_top.iloc[0]['Player'].split(' (')[0]}", f"{qb_top.iloc[0]['FPTS']:.1f} pts")
                else:
                    st.metric("🏈 Top QB", "N/A", "No data")
        except Exception as e:
            st.metric("🏈 Top QB", "Error", str(e)[:20])
    
    with col2:
        try:
            if selected_weeks and len(selected_weeks) < 18:
                rb_data = get_filtered_data(analyzer, selected_weeks, 'RB')
                if rb_data is not None and not rb_data.empty:
                    top_rb = rb_data.iloc[0]
                    st.metric("🏃‍♂️ Top RB", f"{top_rb['Player'].split(' (')[0]}", f"{top_rb['Total_FPTS']:.1f} pts")
                else:
                    st.metric("🏃‍♂️ Top RB", "N/A", "No data")
            else:
                rb_top = analyzer.get_top_performers('RB', week=None, top_n=1)
                if rb_top is not None and not rb_top.empty:
                    st.metric("🏃‍♂️ Top RB", f"{rb_top.iloc[0]['Player'].split(' (')[0]}", f"{rb_top.iloc[0]['FPTS']:.1f} pts")
                else:
                    st.metric("🏃‍♂️ Top RB", "N/A", "No data")
        except Exception as e:
            st.metric("🏃‍♂️ Top RB", "Error", str(e)[:20])
    
    with col3:
        try:
            if selected_weeks and len(selected_weeks) < 18:
                wr_data = get_filtered_data(analyzer, selected_weeks, 'WR')
                if wr_data is not None and not wr_data.empty:
                    top_wr = wr_data.iloc[0]
                    st.metric("🎯 Top WR", f"{top_wr['Player'].split(' (')[0]}", f"{top_wr['Total_FPTS']:.1f} pts")
                else:
                    st.metric("🎯 Top WR", "N/A", "No data")
            else:
                wr_top = analyzer.get_top_performers('WR', week=None, top_n=1)
                if wr_top is not None and not wr_top.empty:
                    st.metric("🎯 Top WR", f"{wr_top.iloc[0]['Player'].split(' (')[0]}", f"{wr_top.iloc[0]['FPTS']:.1f} pts")
                else:
                    st.metric("🎯 Top WR", "N/A", "No data")
        except Exception as e:
            st.metric("🎯 Top WR", "Error", str(e)[:20])
    
    with col4:
        try:
            if selected_weeks and len(selected_weeks) < 18:
                te_data = get_filtered_data(analyzer, selected_weeks, 'TE')
                if te_data is not None and not te_data.empty:
                    top_te = te_data.iloc[0]
                    st.metric("🎪 Top TE", f"{top_te['Player'].split(' (')[0]}", f"{top_te['Total_FPTS']:.1f} pts")
                else:
                    st.metric("🎪 Top TE", "N/A", "No data")
            else:
                te_top = analyzer.get_top_performers('TE', week=None, top_n=1)
                if te_top is not None and not te_top.empty:
                    st.metric("🎪 Top TE", f"{te_top.iloc[0]['Player'].split(' (')[0]}", f"{te_top.iloc[0]['FPTS']:.1f} pts")
                else:
                    st.metric("🎪 Top TE", "N/A", "No data")
        except Exception as e:
            st.metric("🎪 Top TE", "Error", str(e)[:20])
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Fallback display in case metrics don't show
    st.markdown("""
    <div style="background: #f9fafb; padding: 1rem; border-radius: 0.5rem; margin: 1rem 0; border: 1px solid #e5e7eb;">
        <h4 style="color: #374151; margin-bottom: 0.5rem;">📊 Quick Stats:</h4>
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem;">
            <div style="text-align: center; padding: 0.5rem; background: white; border-radius: 0.25rem; border: 1px solid #d1d5db;">
                <div style="font-weight: 600; color: #1e3a8a;">🏈 QB</div>
                <div style="color: #6b7280;">Lamar Jackson</div>
                <div style="color: #059669; font-weight: 600;">460.8 pts</div>
            </div>
            <div style="text-align: center; padding: 0.5rem; background: white; border-radius: 0.25rem; border: 1px solid #d1d5db;">
                <div style="font-weight: 600; color: #1e3a8a;">🏃‍♂️ RB</div>
                <div style="color: #6b7280;">Saquon Barkley</div>
                <div style="color: #059669; font-weight: 600;">361.8 pts</div>
            </div>
            <div style="text-align: center; padding: 0.5rem; background: white; border-radius: 0.25rem; border: 1px solid #d1d5db;">
                <div style="font-weight: 600; color: #1e3a8a;">🎯 WR</div>
                <div style="color: #6b7280;">Ja'Marr Chase</div>
                <div style="color: #059669; font-weight: 600;">291.6 pts</div>
            </div>
            <div style="text-align: center; padding: 0.5rem; background: white; border-radius: 0.25rem; border: 1px solid #d1d5db;">
                <div style="font-weight: 600; color: #1e3a8a;">🎪 TE</div>
                <div style="color: #6b7280;">George Kittle</div>
                <div style="color: #059669; font-weight: 600;">190.8 pts</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Top performers by position
    st.markdown('<h3 class="subsection-header">🏆 Top Performers by Position</h3>', unsafe_allow_html=True)
    
    tabs = st.tabs(["QB", "RB", "WR", "TE"])
    
    for i, position in enumerate(['QB', 'RB', 'WR', 'TE']):
        with tabs[i]:
            if selected_weeks and len(selected_weeks) < 18:
                # Use filtered data
                position_data = get_filtered_data(analyzer, selected_weeks, position)
                if position_data is not None:
                    fig = create_top_performers_chart(position_data, position, f"Top 10 {position}s", selected_weeks)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Show data table
                    st.subheader(f"Top 10 {position}s Data")
                    st.dataframe(position_data.head(10), use_container_width=True)
            else:
                # Use season data
                top_performers = analyzer.get_top_performers(position, week=None, top_n=10)
                if top_performers is not None:
                    fig = create_top_performers_chart(top_performers, position, f"Top 10 {position}s")
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Show data table
                    st.subheader(f"Top 10 {position}s Data")
                    st.dataframe(top_performers, use_container_width=True)

def show_position_analysis(analyzer, selected_weeks):
    """Show position-specific analysis"""
    st.markdown('<h2 class="section-header">🎯 Position Analysis</h2>', unsafe_allow_html=True)
    
    position = st.selectbox("Select Position:", ['QB', 'RB', 'WR', 'TE'])
    
    # Top performers
    st.markdown(f'<h3 class="subsection-header">🏆 Top 10 {position}s</h3>', unsafe_allow_html=True)
    
    if selected_weeks and len(selected_weeks) < 18:
        # Use filtered data
        position_data = get_filtered_data(analyzer, selected_weeks, position)
        if position_data is not None:
            fig = create_top_performers_chart(position_data, position, f"Top 10 {position}s", selected_weeks)
            st.plotly_chart(fig, use_container_width=True)
            
            # Show data table
            st.dataframe(position_data.head(10), use_container_width=True)
    else:
        # Use season data
        top_performers = analyzer.get_top_performers(position, week=None, top_n=10)
        if top_performers is not None:
            fig = create_top_performers_chart(top_performers, position, f"Top 10 {position}s")
            st.plotly_chart(fig, use_container_width=True)
            
            # Show data table
            st.dataframe(top_performers, use_container_width=True)

def show_weekly_trends(analyzer, selected_weeks):
    """Show weekly trends analysis"""
    st.markdown('<h2 class="section-header">📈 Weekly Trends</h2>', unsafe_allow_html=True)
    
    position = st.selectbox("Select Position:", ['QB', 'RB', 'WR', 'TE'])
    top_n = st.slider("Number of top players to show:", 3, 10, 5)
    
    # Weekly trends chart
    fig = create_weekly_trends_chart(analyzer, position, top_n, selected_weeks)
    st.plotly_chart(fig, use_container_width=True)
    
    # Weekly summary
    if selected_weeks and len(selected_weeks) < 18:
        st.subheader(f"Weekly Summary ({len(selected_weeks)} weeks)")
        for week in selected_weeks:
            if week in analyzer.weekly_data and position in analyzer.weekly_data[week]:
                df = analyzer.weekly_data[week][position]
                top_3 = df.nlargest(3, 'FPTS')[['Player', 'FPTS']]
                st.write(f"**{week} - Top 3 {position}s:**")
                st.dataframe(top_3, use_container_width=True)

def show_consistency_analysis(analyzer, selected_weeks):
    """Show consistency analysis"""
    st.markdown('<h2 class="section-header">🎯 Consistency Analysis</h2>', unsafe_allow_html=True)
    
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
    
    consistency = analyzer.get_consistency_analysis(position, min_games=min_games)
    
    if not consistency.empty:
        # Consistency chart
        fig = create_consistency_chart(consistency, position)
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed consistency data
        st.subheader("Detailed Consistency Analysis")
        st.dataframe(consistency, use_container_width=True)
        
        # Consistency insights
        st.subheader("Key Insights")
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
        <h3 style="color: #1e3a8a; margin-bottom: 1rem; text-align: center;">🏈 Fantasy Football Analysis Dashboard</h3>
        
        <p style="font-size: 1.1rem; color: #374151; margin-bottom: 1.5rem;">
            This interactive dashboard provides comprehensive analysis of fantasy football data from FantasyPros.
        </p>
        
        <h4 style="color: #059669; margin-bottom: 0.5rem;">✨ Features:</h4>
        <ul style="color: #6b7280; margin-bottom: 1.5rem;">
            <li><strong>Season Overview:</strong> Top performers and position comparisons</li>
            <li><strong>Position Analysis:</strong> Detailed analysis for each position (QB, RB, WR, TE)</li>
            <li><strong>Weekly Trends:</strong> Track player performance over time</li>
            <li><strong>Consistency Analysis:</strong> Identify reliable players</li>
            <li><strong>Week Filtering:</strong> Analyze specific weeks or week ranges</li>
        </ul>
        
        <h4 style="color: #059669; margin-bottom: 0.5rem;">🛠️ Technology:</h4>
        <ul style="color: #6b7280; margin-bottom: 1.5rem;">
            <li>Built with <strong>Streamlit</strong></li>
            <li>Interactive <strong>Plotly</strong> charts</li>
            <li>Real-time data analysis</li>
            <li>Advanced filtering capabilities</li>
        </ul>
        
        <h4 style="color: #059669; margin-bottom: 0.5rem;">🚀 Deployment:</h4>
        <p style="color: #6b7280; margin-bottom: 1.5rem;">
            This dashboard is designed to be deployed on Streamlit Cloud or any web hosting service.
        </p>
        
        <h4 style="color: #059669; margin-bottom: 0.5rem;">👨‍💻 Author:</h4>
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