import os
import pandas as pd
from weasyprint import HTML
from src.data_processor import (
    load_socialmedia_csv, load_top5_csv,
    get_summary_metrics, get_platform_breakdown,
    get_weekly_trends
)

def generate_pdf_report(output_path="reports/summary_report.pdf"):
    # Ensure output folder exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Load data
    social_df = load_socialmedia_csv("data/input/socialmedia.csv")
    top5_df = load_top5_csv("data/input/top5.csv")

    # Summary metrics
    alltime_metrics = get_summary_metrics(social_df, alltime=True)

    # Weekly summary data
    df_weekly = social_df.iloc[4:].reset_index(drop=True)
    platforms = df_weekly['platform'].unique()

    # Top 5 latest posts
    top5_recent = top5_df.tail(5).copy()
    top5_recent['Label'] = [f"{i+1}. {pt}" for i, pt in enumerate(top5_recent['Post Type'])]

    # Helper functions
    def calc_percent_change(current, previous):
        if previous == 0: return float('inf') if current != 0 else 0
        return ((current - previous) / previous) * 100

    def format_percent(percent):
        if percent == float('inf'): return "+∞%"
        elif percent == 0: return "0%"
        elif percent > 0: return f"+{percent:.1f}%"
        else: return f"{percent:.1f}%"

    # Build HTML
    html = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
                color: #333;
            }}
            h1, h2, h3 {{
                color: #1f77b4;
            }}
            .metrics {{
                display: flex;
                justify-content: space-between;
                margin-bottom: 40px;
            }}
            .metric-card {{
                background: #f9f9f9;
                border-radius: 8px;
                padding: 20px;
                width: 30%;
                text-align: center;
                box-shadow: 0 0 5px #ddd;
            }}
            .metric-value {{
                font-size: 28px;
                font-weight: bold;
            }}
            .metric-label {{
                font-size: 16px;
                color: #666;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 40px;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 10px;
                text-align: center;
            }}
            th {{
                background-color: #f0f8ff;
            }}
            .top5-post {{
                background: #f9f9f9;
                border-radius: 8px;
                padding: 15px;
                margin-bottom: 15px;
                box-shadow: 0 0 5px #ddd;
            }}
            .top5-link {{
                color: #1f77b4;
                text-decoration: none;
                font-weight: bold;
            }}
            .top5-label {{
                font-weight: bold;
                font-size: 16px;
            }}
        </style>
    </head>
    <body>
        <h1>Content Performance Dashboard Report</h1>

        <h2>All-Time Summary Metrics</h2>
        <div class="metrics">
            <div class="metric-card">
                <div class="metric-label">Total Views (All-Time)</div>
                <div class="metric-value">{alltime_metrics['total_views']:,}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Total Likes (All-Time)</div>
                <div class="metric-value">{alltime_metrics['total_likes']:,}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Total Follower Growth (All-Time)</div>
                <div class="metric-value">{alltime_metrics['total_follower_growth']:,}</div>
            </div>
        </div>

        <h2>Weekly Summary Metrics (Latest Week)</h2>
        <table>
            <thead>
                <tr>
                    <th>Platform</th>
                    <th>Views</th>
                    <th>Likes</th>
                    <th>Follower Growth</th>
                    <th>Views % Change</th>
                    <th>Likes % Change</th>
                    <th>Follower Growth % Change</th>
                </tr>
            </thead>
            <tbody>
    """

    for platform in platforms:
        current_row = df_weekly[df_weekly['platform'] == platform].iloc[0]
        previous_row = df_weekly[df_weekly['platform'] == platform].iloc[4]

        current_views = int(current_row['views'])
        current_likes = int(current_row['likes'])
        current_followers = int(current_row['follower_growth'])
        prev_views = int(previous_row['views'])
        prev_likes = int(previous_row['likes'])
        prev_followers = int(previous_row['follower_growth'])

        views_percent = calc_percent_change(current_views, prev_views)
        likes_percent = calc_percent_change(current_likes, prev_likes)
        followers_percent = calc_percent_change(current_followers, prev_followers)

        html += f"""
            <tr>
                <td>{platform.title()}</td>
                <td>{current_views:,}</td>
                <td>{current_likes:,}</td>
                <td>{current_followers:,}</td>
                <td>{format_percent(views_percent)}</td>
                <td>{format_percent(likes_percent)}</td>
                <td>{format_percent(followers_percent)}</td>
            </tr>
        """

    html += """
            </tbody>
        </table>

        <h2>Charts and Visualizations</h2>
        <p><em>Note: Charts are not included in the PDF export due to platform limitations.</em></p>

        <h2>Top 5 Posts (Latest Week)</h2>
    """

    for idx, (_, row) in enumerate(top5_recent.iterrows()):
        views = f"{row['Views']:,}"
        engagement = f"{row['Engagement']:,}"
        link = row['Link']
        post_type = row['Post Type']
        html += f"""
        <div class="top5-post">
            <div class="top5-label">{idx + 1}. {post_type}</div>
            <div><a class="top5-link" href="{link}">{link}</a></div>
            <div><strong>{views} views • {engagement} engagement</strong></div>
        </div>
        """

    html += """
    </body>
    </html>
    """

    # Render PDF
    HTML(string=html).write_pdf(output_path)
