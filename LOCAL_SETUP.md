# 🏈 Local Setup Guide

This guide will help you run the Fantasy Football Analysis Dashboard locally before uploading to GitHub.

## ✅ Prerequisites

- Python 3.8+ installed
- Your fantasy football data in the correct format
- All dependencies installed

## 🚀 Quick Start

### Option 1: Use the Launcher (Recommended)
```bash
python run_analysis.py
```
Then choose option **4** for the interactive dashboard.

### Option 2: Run Dashboard Directly
```bash
streamlit run streamlit_app.py
```

### Option 3: Test Everything First
```bash
python test_local.py
```

## 📊 What You'll See

When you run the dashboard, it will:

1. **Open in your web browser** automatically (usually at http://localhost:8501)
2. **Load your fantasy football data** (18 weeks of data)
3. **Display interactive charts** and analysis
4. **Allow you to explore** different positions and metrics

## 🎯 Dashboard Features

### Overview Page
- **Season leaders** for each position
- **Key metrics** displayed prominently
- **Position comparison** charts
- **Top performers** tables

### Position Analysis
- **Interactive charts** for each position
- **Top 10 players** with fantasy points
- **Detailed statistics** in tables
- **Filtering options**

### Consistency Analysis
- **Most consistent players** identified
- **Consistency scoring** system
- **Risk assessment** for roster decisions
- **Detailed breakdowns**

## 🔧 Troubleshooting

### If the dashboard doesn't open automatically:
1. Check your terminal for the URL (usually http://localhost:8501)
2. Open that URL in your web browser manually

### If you get import errors:
```bash
pip install -r requirements.txt
```

### If data doesn't load:
1. Verify your data path: `/Users/hannesschiller/Documents/NFL Fantasy data`
2. Check that your data follows the expected structure
3. The app will use sample data if your data isn't found

### If Streamlit has issues:
```bash
pip install --upgrade streamlit
```

## 📱 Using the Dashboard

### Navigation
- Use the **sidebar** to switch between pages
- **Overview**: Get a quick snapshot of everything
- **Position Analysis**: Deep dive into specific positions
- **Consistency Analysis**: Find reliable players
- **About**: Information about the dashboard

### Interactive Features
- **Hover over charts** for detailed information
- **Click and drag** to zoom in on charts
- **Use filters** to narrow down results
- **Download data** from tables

### Key Insights
- **Top performers** by position
- **Consistency scores** for reliability
- **Weekly trends** for momentum
- **Value analysis** for roster decisions

## 🎉 Success Indicators

You'll know everything is working when you see:
- ✅ "Data loaded successfully!" message
- ✅ Interactive charts with your data
- ✅ Top performers like Lamar Jackson, Saquon Barkley, etc.
- ✅ Smooth navigation between pages
- ✅ Responsive design on different screen sizes

## 📋 Before Uploading to GitHub

1. **Test the dashboard** thoroughly
2. **Verify all features** work as expected
3. **Check data accuracy** matches your expectations
4. **Run the test suite**: `python test_local.py`
5. **Document any issues** or customizations needed

## 🚀 Ready for Deployment

Once you're satisfied with the local version:

1. **Run the deployment script**: `python deploy.py`
2. **Create GitHub repository**
3. **Push your code**
4. **Deploy to Streamlit Cloud**
5. **Share your live dashboard!**

---

**Happy analyzing! 🏈📊** 