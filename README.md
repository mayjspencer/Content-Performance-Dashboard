# Content Performance Dashboard
A streamlined dashboard for visualizing weekly performance across Facebook, TikTok, YouTube, and other platforms. Built to replace messy spreadsheets, this tool helps our small media team quickly identify what’s working, what’s trending, and where to focus next.

- [**Live Demo**](https://boomerbackfield.streamlit.app)

- 🛠️ Python • Streamlit •  Plotly

- Used internally by our startup to track Social Media pages with 45M+ views.

## Features

-  **Multi-Platform Analysis**: Upload weekly `.csv` exports from Facebook, TikTok, and others  
-  **Weekly Metrics Overview**: Total views, reach, and post count  
-  **Multi-Week Trends**: Compare engagement over time with line and bar charts  
-  **Top Performing Posts**: Highlights the week’s 5 best posts  
-  **Upload & Snapshot Ready**: Simple interface for weekly updates

## Dashboard Preview

### Summary Metrics View
![Summary Metrics](assets/summary_metrics.png)

### Top 5 Posts Comparison
![Top 5 Posts](assets/top_posts.png)


## Tech Stack

- **Frontend/UI**: [Streamlit](https://streamlit.io/)
- **Data Analysis**: Python
- **Visualization**: Plotly
- **Deployment**: Streamlit Community Cloud
- **Version Control**: Git + GitHub

## Live Demo

Want to try it yourself?  
 **[Click here to view the live app](https://boomerbackfield.streamlit.app)**

## How to Run Locally

1. Clone this repo:
```bash
git clone https://github.com/mayjspencer/content-performance-dashboard.git
cd content-performance-dashboard
```

2. Set up a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Run the app:
```bash
streamlit run dashboard.py
```

## Sample Data

This app is designed to work with .csv files exported from platform insights (e.g., Facebook Creator Studio, X Analytics, etc.)

See the data/input folder for mock files to try the app locally.
