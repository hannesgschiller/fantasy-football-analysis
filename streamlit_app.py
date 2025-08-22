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

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
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
    .week-filter {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
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
        st.info("📊 Using sample data for demonstration. To use real data, add your fantasy football data files to the project.")
        return create_sample_data()
    
    try:
        analyzer = FantasyFootballAnalyzer(data_path)
        analyzer.load_weekly_data()
        analyzer.load_season_data()
        st.success(f"✅ Loaded data from: {data_path}")
        return analyzer
    except Exception as e:
        st.warning(f"⚠️ Error loading data from {data_path}: {str(e)}")
        st.info("📊 Falling back to sample data for demonstration.")
        return create_sample_data()

def create_sample_data():
    """Create sample data for demonstration"""
    class SampleAnalyzer:
        def __init__(self):
            self.positions = ['QB', 'RB', 'WR', 'TE']
            self.weekly_data = {}
            self.season_data = {}
            
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
            
            # Create sample weekly data for all 18 weeks
            for week in range(1, 19):  # Full 18-week season
                week_name = f"Week {week}"
                self.weekly_data[week_name] = {}
                
                for position in self.positions:
                    # Create sample weekly data for each position with realistic variations
                    if position == 'QB':
                        # Add some randomness and realistic weekly variations
                        base_scores = [25.6, 22.7, 22.5, 22.2, 22.1]
                        weekly_variation = np.random.normal(0, 5)  # Random weekly variation
                        df = pd.DataFrame({
                            'Player': ['Lamar Jackson (BAL)', 'Josh Allen (BUF)', 'Joe Burrow (CIN)', 'Patrick Mahomes (KC)', 'Jalen Hurts (PHI)'],
                            'FPTS': [max(0, base + weekly_variation + np.random.normal(0, 3)) for base in base_scores],
                            'FPTS/G': base_scores
                        })
                    elif position == 'RB':
                        base_scores = [20.1, 18.7, 18.3, 18.2, 17.9]
                        weekly_variation = np.random.normal(0, 4)
                        df = pd.DataFrame({
                            'Player': ['Saquon Barkley (PHI)', 'Derrick Henry (BAL)', 'Jahmyr Gibbs (DET)', 'Christian McCaffrey (SF)', 'Alvin Kamara (NO)'],
                            'FPTS': [max(0, base + weekly_variation + np.random.normal(0, 2.5)) for base in base_scores],
                            'FPTS/G': base_scores
                        })
                    elif position == 'WR':
                        base_scores = [16.2, 12.6, 11.8, 11.7, 11.5]
                        weekly_variation = np.random.normal(0, 3)
                        df = pd.DataFrame({
                            'Player': ['Ja\'Marr Chase (CIN)', 'Justin Jefferson (MIN)', 'Amon-Ra St. Brown (DET)', 'Tyreek Hill (MIA)', 'CeeDee Lamb (DAL)'],
                            'FPTS': [max(0, base + weekly_variation + np.random.normal(0, 2)) for base in base_scores],
                            'FPTS/G': base_scores
                        })
                    else:  # TE
                        base_scores = [10.6, 8.9, 8.7, 8.0, 7.8]
                        weekly_variation = np.random.normal(0, 2)
                        df = pd.DataFrame({
                            'Player': ['George Kittle (SF)', 'Brock Bowers (LV)', 'Trey McBride (ARI)', 'Sam LaPorta (DET)', 'Evan Engram (JAX)'],
                            'FPTS': [max(0, base + weekly_variation + np.random.normal(0, 1.5)) for base in base_scores],
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
    st.subheader("📅 Week Filter")
    
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
        st.info(f"Showing data for all {len(selected_weeks)} weeks")
        
    elif filter_type == "Single Week":
        selected_week = st.selectbox("Select Week:", available_weeks)
        selected_weeks = [selected_week]
        st.info(f"Showing data for {selected_week}")
        
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
            st.info(f"Showing data for weeks {start_week} to {end_week} ({len(selected_weeks)} weeks)")
        else:
            st.error("Start week must be before or equal to end week")
            
    elif filter_type == "Custom Selection":
        selected_weeks = st.multiselect(
            "Select Weeks:",
            available_weeks,
            default=available_weeks[:5]  # Default to first 5 weeks
        )
        if selected_weeks:
            st.info(f"Showing data for {len(selected_weeks)} selected weeks")
        else:
            st.warning("Please select at least one week")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return selected_weeks

def create_top_performers_chart(df, position, title, selected_weeks=None):
    """Create a horizontal bar chart for top performers"""
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
    
    fig = go.Figure(data=[
        go.Bar(
            x=values,
            y=players,
            orientation='h',
            marker_color='#1f77b4',
            text=[f"{val:.1f}" for val in values],
            textposition='auto',
        )
    ])
    
    # Add week info to title if filtering
    if selected_weeks and len(selected_weeks) < 18:
        if len(selected_weeks) == 1:
            title += f" - {selected_weeks[0]}"
        else:
            title += f" - {len(selected_weeks)} weeks"
    
    fig.update_layout(
        title=title,
        xaxis_title=value_label,
        yaxis_title="Players",
        height=400,
        showlegend=False,
        yaxis={'categoryorder': 'total ascending'}
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

def create_weekly_trends_chart(analyzer, position, top_n=5, selected_weeks=None):
    """Create weekly trends chart for top players"""
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
    
    # Add week info to title if filtering
    title = f'{position} Weekly Performance Trends - Top {top_n} Season Performers'
    if selected_weeks and len(selected_weeks) < 18:
        if len(selected_weeks) == 1:
            title += f" ({selected_weeks[0]})"
        else:
            title += f" ({len(selected_weeks)} weeks)"
    
    fig.update_layout(
        title=title,
        xaxis_title='Week',
        yaxis_title='Fantasy Points',
        height=400,
        hovermode='x unified'
    )
    
    return fig

def main():
    """Main dashboard function"""
    
    # Header
    st.markdown('<h1 class="main-header">🏈 Fantasy Football Analysis Dashboard</h1>', unsafe_allow_html=True)
    
    # Load data with progress indicator
    with st.spinner('Loading fantasy football data...'):
        analyzer = load_data()
    
    st.success("✅ Data loaded successfully!")
    
    # Week filter
    selected_weeks = create_week_filter()
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
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
    st.header("📊 Season Overview")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if selected_weeks and len(selected_weeks) < 18:
            # Use filtered data for top QB
            qb_data = get_filtered_data(analyzer, selected_weeks, 'QB')
            if qb_data is not None and not qb_data.empty:
                top_qb = qb_data.iloc[0]
                st.metric("Top QB", f"{top_qb['Player'].split(' (')[0]}", f"{top_qb['Total_FPTS']:.1f} pts")
            else:
                st.metric("Top QB", "N/A", "No data")
        else:
            # Use season data
            qb_top = analyzer.get_top_performers('QB', week=None, top_n=1)
            if qb_top is not None:
                st.metric("Top QB", f"{qb_top.iloc[0]['Player'].split(' (')[0]}", f"{qb_top.iloc[0]['FPTS']:.1f} pts")
    
    with col2:
        if selected_weeks and len(selected_weeks) < 18:
            rb_data = get_filtered_data(analyzer, selected_weeks, 'RB')
            if rb_data is not None and not rb_data.empty:
                top_rb = rb_data.iloc[0]
                st.metric("Top RB", f"{top_rb['Player'].split(' (')[0]}", f"{top_rb['Total_FPTS']:.1f} pts")
            else:
                st.metric("Top RB", "N/A", "No data")
        else:
            rb_top = analyzer.get_top_performers('RB', week=None, top_n=1)
            if rb_top is not None:
                st.metric("Top RB", f"{rb_top.iloc[0]['Player'].split(' (')[0]}", f"{rb_top.iloc[0]['FPTS']:.1f} pts")
    
    with col3:
        if selected_weeks and len(selected_weeks) < 18:
            wr_data = get_filtered_data(analyzer, selected_weeks, 'WR')
            if wr_data is not None and not wr_data.empty:
                top_wr = wr_data.iloc[0]
                st.metric("Top WR", f"{top_wr['Player'].split(' (')[0]}", f"{top_wr['Total_FPTS']:.1f} pts")
            else:
                st.metric("Top WR", "N/A", "No data")
        else:
            wr_top = analyzer.get_top_performers('WR', week=None, top_n=1)
            if wr_top is not None:
                st.metric("Top WR", f"{wr_top.iloc[0]['Player'].split(' (')[0]}", f"{wr_top.iloc[0]['FPTS']:.1f} pts")
    
    with col4:
        if selected_weeks and len(selected_weeks) < 18:
            te_data = get_filtered_data(analyzer, selected_weeks, 'TE')
            if te_data is not None and not te_data.empty:
                top_te = te_data.iloc[0]
                st.metric("Top TE", f"{top_te['Player'].split(' (')[0]}", f"{top_te['Total_FPTS']:.1f} pts")
            else:
                st.metric("Top TE", "N/A", "No data")
        else:
            te_top = analyzer.get_top_performers('TE', week=None, top_n=1)
            if te_top is not None:
                st.metric("Top TE", f"{te_top.iloc[0]['Player'].split(' (')[0]}", f"{te_top.iloc[0]['FPTS']:.1f} pts")
    
    # Top performers by position
    st.subheader("Top Performers by Position")
    
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
    st.header("🎯 Position Analysis")
    
    position = st.selectbox("Select Position:", ['QB', 'RB', 'WR', 'TE'])
    
    # Top performers
    st.subheader(f"Top 10 {position}s")
    
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
    st.header("📈 Weekly Trends")
    
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
    st.header("🎯 Consistency Analysis")
    
    position = st.selectbox("Select Position:", ['QB', 'RB', 'WR', 'TE'])
    min_games = st.slider("Minimum games played:", 3, 10, 5)
    
    # Note: Consistency analysis works best with full season data
    # For filtered weeks, we'll show a note
    if selected_weeks and len(selected_weeks) < 18:
        st.info(f"📝 Note: Consistency analysis is shown for the full season. You're currently filtering {len(selected_weeks)} weeks.")
    
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
    st.header("ℹ️ About This Dashboard")
    
    st.markdown("""
    ## Fantasy Football Analysis Dashboard
    
    This interactive dashboard provides comprehensive analysis of fantasy football data from FantasyPros.
    
    ### Features:
    - **Season Overview**: Top performers and position comparisons
    - **Position Analysis**: Detailed analysis for each position (QB, RB, WR, TE)
    - **Weekly Trends**: Track player performance over time
    - **Consistency Analysis**: Identify reliable players
    - **Week Filtering**: Analyze specific weeks or week ranges
    
    ### Technology:
    - Built with Streamlit
    - Interactive Plotly charts
    - Real-time data analysis
    - Advanced filtering capabilities
    
    ### Deployment:
    This dashboard is designed to be deployed on Streamlit Cloud or any web hosting service.
    
    ### Author:
    Professional fantasy football analysis tool for data-driven decision making.
    """)
    
    st.markdown("---")
    st.markdown("**GitHub Repository**: [Add your GitHub link here]")
    st.markdown("**Contact**: [Add your contact information here]")

if __name__ == "__main__":
    main() 