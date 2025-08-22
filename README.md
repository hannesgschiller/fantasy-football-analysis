# Fantasy Football Analysis Dashboard

A comprehensive, interactive fantasy football analysis dashboard built with Streamlit and Python. This tool provides detailed insights into player performance, trends, and value analysis across all positions (QB, RB, WR, TE).

## 🚀 Live Demo

(https://fantasy-football-analysis-7ciw66tausuytwvldxwzde.streamlit.app/)

## ✨ Features

### 📊 Core Analysis
- **Interactive Dashboard**: Real-time data exploration with Streamlit
- **Weekly Performance Tracking**: Analyze player performance week by week
- **Season-Long Statistics**: Comprehensive season statistics and rankings
- **Position Comparisons**: Compare top performers across all positions
- **Consistency Analysis**: Identify the most consistent players

### 🎯 Advanced Insights
- **Breakout Players**: Find players who have significantly improved their performance
- **Value Analysis**: Identify players providing the best value relative to roster percentage
- **Volatility Analysis**: Find the most inconsistent players (high risk/reward)
- **Emerging Trends**: Identify players trending upward in recent weeks

### 📈 Interactive Visualizations
- **Dynamic Charts**: Interactive Plotly visualizations
- **Position Dashboards**: Comprehensive analysis for each position
- **Weekly Trend Charts**: Track player performance over time
- **Real-time Filtering**: Filter and explore data dynamically

## 🛠️ Installation

### Local Development

1. **Clone the repository**:
   ```bash
   git clone https://github.com/hannesgschiller/fantasy-football-analysis.git
   cd fantasy-football-analysis
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the dashboard**:
   ```bash
   streamlit run streamlit_app.py
   ```

### Data Setup

Ensure your fantasy football data is organized as follows:
```
NFL Fantasy data/
├── Week 1/
│   ├── FantasyPros_Fantasy_Football_Statistics_QB (1).csv
│   ├── FantasyPros_Fantasy_Football_Statistics_RB (1).csv
│   ├── FantasyPros_Fantasy_Football_Statistics_WR (1).csv
│   └── FantasyPros_Fantasy_Football_Statistics_TE (1).csv
├── Week 2/
│   └── ...
├── Full Season/
│   ├── FantasyPros_Fantasy_Football_Statistics_QB.csv
│   ├── FantasyPros_Fantasy_Football_Statistics_RB.csv
│   ├── FantasyPros_Fantasy_Football_Statistics_WR.csv
│   └── FantasyPros_Fantasy_Football_Statistics_TE.csv
```

## 🌐 Deployment

### Streamlit Cloud (Recommended)

1. **Push to GitHub**: Ensure your code is in a public GitHub repository
2. **Connect to Streamlit Cloud**: 
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Select your repository
   - Set the main file path to `streamlit_app.py`
   - Deploy!

### Heroku

1. **Create Procfile**:
   ```
   web: streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. **Deploy**:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

### Docker

1. **Create Dockerfile**:
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   EXPOSE 8501
   CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
   ```

2. **Build and run**:
   ```bash
   docker build -t fantasy-football-dashboard .
   docker run -p 8501:8501 fantasy-football-dashboard
   ```

## 📁 Project Structure

```
fantasy_football_analysis/
├── streamlit_app.py              # Main Streamlit application
├── dashboard.py                   # Full-featured dashboard
├── fantasy_analyzer_simple.py     # Core analysis engine
├── advanced_analysis.py           # Advanced analysis features
├── quick_analysis.py              # Interactive CLI tool
├── run_analysis.py                # Launcher script
├── requirements.txt               # Python dependencies
├── README.md                      # This file
├── .gitignore                     # Git ignore rules
└── data/                          # Data directory (not in repo)
    └── NFL Fantasy data/
```

## 🎮 Usage

### Interactive Dashboard
1. **Overview**: Get a quick snapshot of top performers across all positions
2. **Position Analysis**: Deep dive into specific positions with detailed charts
3. **Consistency Analysis**: Find the most reliable players for your roster
4. **Player Search**: Search for specific players and their statistics

### Command Line Tools
```bash
# Run basic analysis
python fantasy_analyzer_simple.py

# Run interactive analysis
python quick_analysis.py

# Run advanced analysis
python advanced_analysis.py

# Use the launcher
python run_analysis.py
```

## 🔧 Customization

### Adding New Analysis Types
Extend the `FantasyFootballAnalyzer` class to add new analysis methods:

```python
def analyze_custom_metric(self, position):
    """Add your custom analysis here"""
    # Your analysis logic
    return results
```

### Modifying Visualizations
Update the chart creation functions in `dashboard.py` to customize visualizations:

```python
def create_custom_chart(data):
    """Create custom visualization"""
    fig = go.Figure()
    # Your chart configuration
    return fig
```

## 📊 Data Requirements

The tool expects FantasyPros CSV files with the following columns:
- `Player`: Player name and team
- `FPTS`: Fantasy points
- `FPTS/G`: Fantasy points per game
- `G`: Games played
- `ROST`: Roster percentage
- Position-specific statistics (passing yards, rushing yards, etc.)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **FantasyPros**: Data source for fantasy football statistics
- **Streamlit**: Web application framework
- **Plotly**: Interactive visualization library
- **Pandas**: Data manipulation and analysis

## 📞 Contact

- **GitHub**: [@hannesgschiller](https://github.com/hannesgschiller)
- **LinkedIn**: https://www.linkedin.com/in/hannes-schiller-b1301b134/
- **Email**: Hannesgschiller@gmail.com

## 🚀 Quick Start for Professional Website

1. **Deploy to Streamlit Cloud** (easiest option)
2. **Embed in your website**:
   ```html
   <iframe src="https://your-app-name.streamlit.app" 
           width="100%" 
           height="800px" 
           frameborder="0">
   </iframe>
   ```
3. **Add to your portfolio** with a link to the live dashboard

---

**Happy analyzing! 🏈📊**
