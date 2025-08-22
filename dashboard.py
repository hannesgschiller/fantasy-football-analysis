#!/usr/bin/env python3
"""
Fantasy Football Interactive Dashboard
A comprehensive Streamlit dashboard for fantasy football analysis
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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
    page_title="Fantasy Football Analysis Dashboard",
    page_icon="🏈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .position-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 1rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1f77b4;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load fantasy football data with caching"""
    data_path = "/Users/hannesschiller/Documents/NFL Fantasy data"
    analyzer = FantasyFootballAnalyzer(data_path)
    analyzer.load_weekly_data()
    analyzer.load_season_data()
    return analyzer

def create_top_performers_chart(df, position, title):
    """Create a horizontal bar chart for top performers"""
    if df is None or df.empty:
        return go.Figure()
    
    # Extract player names (remove team info)
    players = [p.split(' (')[0] if ' (' in p else p for p in df['Player']]
    
    fig = go.Figure(data=[
        go.Bar(
            x=df['FPTS'],
            y=players,
            orientation='h',
            marker_color='#1f77b4',
            text=[f"{val:.1f}" for val in df['FPTS']],
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title=title,
        xaxis_title="Fantasy Points",
        yaxis_title="Players",
        height=400,
        showlegend=False,
        yaxis={'categoryorder': 'total ascending'}
    )
    
    return fig

def create_weekly_trends_chart(analyzer, position, top_n=5):
    """Create weekly trends chart for top players"""
    # Get top players for the season
    season_top = analyzer.get_top_performers(position, week=None, top_n=top_n)
    if season_top is None:
        return go.Figure()
    
    top_players = [p.split(' (')[0] if ' (' in p else p for p in season_top['Player']]
    
    # Track their weekly performance
    weekly_performance = {}
    for player in top_players:
        weekly_performance[player] = []
    
    weeks = sorted(analyzer.weekly_data.keys())
    for week in weeks:
        if position in analyzer.weekly_data[week]:
            df = analyzer.weekly_data[week][position]
            for player in top_players:
                # Find player in this week's data
                player_row = df[df['Player'].str.contains(player, na=False)]
                if not player_row.empty:
                    weekly_performance[player].append(player_row.iloc[0]['FPTS'])
                else:
                    weekly_performance[player].append(0)
    
    # Create the plot
    fig = go.Figure()
    
    for player, performance in weekly_performance.items():
        fig.add_trace(go.Scatter(
            x=list(range(1, len(performance) + 1)),
            y=performance,
            mode='lines+markers',
            name=player,
            line=dict(width=2)
        ))
    
    fig.update_layout(
        title=f'{position} Weekly Performance Trends',
        xaxis_title='Week',
        yaxis_title='Fantasy Points',
        height=400,
        hovermode='x unified'
    )
    
    return fig

def create_consistency_chart(consistency_df, position):
    """Create consistency analysis chart"""
    if consistency_df.empty:
        return go.Figure()
    
    top_10 = consistency_df.head(10)
    
    fig = go.Figure(data=[
        go.Bar(
            x=top_10['Consistency_Score'],
            y=top_10['Player'],
            orientation='h',
            marker_color='#2ca02c',
            text=[f"{val:.2f}" for val in top_10['Consistency_Score']],
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title=f'Most Consistent {position}s',
        xaxis_title="Consistency Score (Higher = More Consistent)",
        yaxis_title="Players",
        height=400,
        showlegend=False,
        yaxis={'categoryorder': 'total ascending'}
    )
    
    return fig

def create_position_comparison(analyzer):
    """Create position comparison chart"""
    position_data = []
    
    for position in analyzer.positions:
        top_performers = analyzer.get_top_performers(position, week=None, top_n=5)
        if top_performers is not None:
            for _, row in top_performers.iterrows():
                player_name = row['Player'].split(' (')[0] if ' (' in row['Player'] else row['Player']
                position_data.append({
                    'Position': position,
                    'Player': player_name,
                    'FPTS': row['FPTS'],
                    'FPTS_G': row['FPTS/G']
                })
    
    df = pd.DataFrame(position_data)
    
    fig = px.bar(df, x='Position', y='FPTS', color='Player',
                 title='Top 5 Players by Position - Season Comparison',
                 height=500)
    
    fig.update_layout(
        xaxis_title="Position",
        yaxis_title="Fantasy Points",
        showlegend=True
    )
    
    return fig

def main():
    """Main dashboard function"""
    
    # Header
    st.markdown('<h1 class="main-header">🏈 Fantasy Football Analysis Dashboard</h1>', unsafe_allow_html=True)
    
    # Load data with progress indicator
    with st.spinner('Loading fantasy football data...'):
        analyzer = load_data()
    
    st.success(f"✅ Loaded data for {len(analyzer.weekly_data)} weeks across all positions")
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page:",
        ["Overview", "Position Analysis", "Weekly Trends", "Consistency Analysis", "Player Search", "About"]
    )
    
    if page == "Overview":
        show_overview(analyzer)
    elif page == "Position Analysis":
        show_position_analysis(analyzer)
    elif page == "Weekly Trends":
        show_weekly_trends(analyzer)
    elif page == "Consistency Analysis":
        show_consistency_analysis(analyzer)
    elif page == "Player Search":
        show_player_search(analyzer)
    elif page == "About":
        show_about()

def show_overview(analyzer):
    """Show overview page"""
    st.header("📊 Season Overview")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        qb_top = analyzer.get_top_performers('QB', week=None, top_n=1)
        if qb_top is not None:
            st.metric("Top QB", f"{qb_top.iloc[0]['Player'].split(' (')[0]}", f"{qb_top.iloc[0]['FPTS']:.1f} pts")
    
    with col2:
        rb_top = analyzer.get_top_performers('RB', week=None, top_n=1)
        if rb_top is not None:
            st.metric("Top RB", f"{rb_top.iloc[0]['Player'].split(' (')[0]}", f"{rb_top.iloc[0]['FPTS']:.1f} pts")
    
    with col3:
        wr_top = analyzer.get_top_performers('WR', week=None, top_n=1)
        if wr_top is not None:
            st.metric("Top WR", f"{wr_top.iloc[0]['Player'].split(' (')[0]}", f"{wr_top.iloc[0]['FPTS']:.1f} pts")
    
    with col4:
        te_top = analyzer.get_top_performers('TE', week=None, top_n=1)
        if te_top is not None:
            st.metric("Top TE", f"{te_top.iloc[0]['Player'].split(' (')[0]}", f"{te_top.iloc[0]['FPTS']:.1f} pts")
    
    # Position comparison chart
    st.subheader("Position Comparison")
    fig = create_position_comparison(analyzer)
    st.plotly_chart(fig, use_container_width=True)
    
    # Top performers by position
    st.subheader("Top Performers by Position")
    
    tabs = st.tabs(["QB", "RB", "WR", "TE"])
    
    for i, position in enumerate(['QB', 'RB', 'WR', 'TE']):
        with tabs[i]:
            top_performers = analyzer.get_top_performers(position, week=None, top_n=10)
            if top_performers is not None:
                fig = create_top_performers_chart(top_performers, position, f"Top 10 {position}s")
                st.plotly_chart(fig, use_container_width=True)
                
                # Show data table
                st.subheader(f"Top 10 {position}s Data")
                st.dataframe(top_performers, use_container_width=True)

def show_position_analysis(analyzer):
    """Show position-specific analysis"""
    st.header("🎯 Position Analysis")
    
    position = st.selectbox("Select Position:", ['QB', 'RB', 'WR', 'TE'])
    
    # Top performers
    st.subheader(f"Top 10 {position}s")
    top_performers = analyzer.get_top_performers(position, week=None, top_n=10)
    if top_performers is not None:
        fig = create_top_performers_chart(top_performers, position, f"Top 10 {position}s")
        st.plotly_chart(fig, use_container_width=True)
    
    # Weekly trends
    st.subheader(f"{position} Weekly Trends")
    top_n = st.slider("Number of top players to show:", 3, 10, 5)
    fig = create_weekly_trends_chart(analyzer, position, top_n)
    st.plotly_chart(fig, use_container_width=True)
    
    # Consistency analysis
    st.subheader(f"{position} Consistency Analysis")
    consistency = analyzer.get_consistency_analysis(position)
    if not consistency.empty:
        fig = create_consistency_chart(consistency, position)
        st.plotly_chart(fig, use_container_width=True)
        
        # Show consistency data
        st.subheader("Consistency Data")
        st.dataframe(consistency.head(10), use_container_width=True)

def show_weekly_trends(analyzer):
    """Show weekly trends analysis"""
    st.header("📈 Weekly Trends")
    
    position = st.selectbox("Select Position:", ['QB', 'RB', 'WR', 'TE'])
    week = st.selectbox("Select Week:", sorted(analyzer.weekly_data.keys()))
    
    # Weekly top performers
    st.subheader(f"{week} - Top {position}s")
    weekly_top = analyzer.get_top_performers(position, week=week, top_n=10)
    if weekly_top is not None:
        fig = create_top_performers_chart(weekly_top, position, f"{week} Top {position}s")
        st.plotly_chart(fig, use_container_width=True)
        
        # Show data
        st.dataframe(weekly_top, use_container_width=True)
    
    # Weekly summary
    st.subheader(f"{week} Summary")
    summary = analyzer.create_weekly_summary(week)
    if summary:
        for pos, data in summary.items():
            st.write(f"**Top 3 {pos}s:**")
            st.dataframe(data, use_container_width=True)

def show_consistency_analysis(analyzer):
    """Show consistency analysis"""
    st.header("🎯 Consistency Analysis")
    
    position = st.selectbox("Select Position:", ['QB', 'RB', 'WR', 'TE'])
    min_games = st.slider("Minimum games played:", 3, 10, 5)
    
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

def show_player_search(analyzer):
    """Show player search functionality"""
    st.header("🔍 Player Search")
    
    # Get all players
    all_players = []
    for position in analyzer.positions:
        if position in analyzer.season_data:
            df = analyzer.season_data[position]
            for _, row in df.iterrows():
                all_players.append({
                    'Player': row['Player'],
                    'Position': position,
                    'FPTS': row.get('FPTS', 0),
                    'FPTS_G': row.get('FPTS/G', 0)
                })
    
    players_df = pd.DataFrame(all_players)
    
    # Search functionality
    search_term = st.text_input("Search for a player:", placeholder="Enter player name...")
    
    if search_term:
        filtered_players = players_df[players_df['Player'].str.contains(search_term, case=False, na=False)]
        
        if not filtered_players.empty:
            st.subheader("Search Results")
            st.dataframe(filtered_players.sort_values('FPTS', ascending=False), use_container_width=True)
            
            # Show player details
            if len(filtered_players) == 1:
                player = filtered_players.iloc[0]
                st.subheader(f"Player Details: {player['Player']}")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Position", player['Position'])
                with col2:
                    st.metric("Total FPTS", f"{player['FPTS']:.1f}")
                with col3:
                    st.metric("FPTS/G", f"{player['FPTS_G']:.1f}")
        else:
            st.warning("No players found matching your search.")

def show_about():
    """Show about page"""
    st.header("ℹ️ About This Dashboard")
    
    st.markdown("""
    ## Fantasy Football Analysis Dashboard
    
    This interactive dashboard provides comprehensive analysis of fantasy football data from FantasyPros.
    
    ### Features:
    - **Season Overview**: Top performers and position comparisons
    - **Position Analysis**: Detailed analysis for each position (QB, RB, WR, TE)
    - **Weekly Trends**: Track player performance over time
    - **Consistency Analysis**: Identify reliable players
    - **Player Search**: Find specific players and their stats
    
    ### Data Source:
    - FantasyPros fantasy football statistics
    - Weekly and season-long data
    - All positions covered (QB, RB, WR, TE)
    
    ### Technology:
    - Built with Streamlit
    - Interactive Plotly charts
    - Real-time data analysis
    
    ### Author:
    Professional fantasy football analysis tool for data-driven decision making.
    """)
    
    st.markdown("---")
    st.markdown("**GitHub Repository**: [Add your GitHub link here]")
    st.markdown("**Contact**: [Add your contact information here]")

if __name__ == "__main__":
    main() 