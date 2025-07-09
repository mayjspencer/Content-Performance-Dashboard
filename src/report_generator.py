import os
import pandas as pd
from weasyprint import HTML
from src.data_processor import (
    load_socialmedia_csv, load_top5_csv,
    get_summary_metrics, get_platform_breakdown,
    get_weekly_trends
)

def generate_pdf_report(output_path="reports/summary_report.pdf"):
    # Ensure output folders exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    os.makedirs("reports/images", exist_ok=True)

    # Load data
    social_df = load_socialmedia_csv("data/input/socialmedia.csv")
    top5_df = load_top5_csv("data/input/top5.csv")

    # Summary metrics
    alltime_metrics = get_summary_metrics(social_df, alltime=True)

    # Weekly summary data for metrics
    df_weekly = social_df.iloc[4:].reset_index(drop=True)
    platforms = df_weekly['platform'].unique()

    # Platform breakdown for last 5 weeks
    platform_data = get_platform_breakdown(social_df)

    # All-time platform data (Instagram excluded)
    alltime_data = social_df[social_df['week'] == 'alltime'].groupby('platform')[['views', 'likes', 'follower_growth']].sum().reset_index()

    # Weekly trends data
    trends_data = get_weekly_trends(social_df)

    # Top 5 latest posts
    top5_recent = top5_df.tail(5).copy()
    top5_recent['Label'] = [f"{i+1}. {pt}" for i, pt in enumerate(top5_recent['Post Type'])]

    # Top 5 comparison data
    latest_top5 = top5_df.tail(5).copy().reset_index(drop=True)
    previous_top5 = top5_df.tail(10).head(5).copy().reset_index(drop=True)
    latest_top5['Week'] = 'This Week'
    previous_top5['Week'] = 'Last Week'
    latest_top5['Rank'] = [f"Post {i+1}" for i in range(5)]
    previous_top5['Rank'] = [f"Post {i+1}" for i in range(5)]
    combined_top5 = pd.concat([latest_top5, previous_top5], ignore_index=True)

    # Helper functions
    def calc_percent_change(current, previous):
        if previous == 0: return float('inf') if current != 0 else 0
        return ((current - previous) / previous) * 100

    def format_percent(percent):
        if percent == float('inf'): return "+∞%"
        elif percent == 0: return "0%"
        elif percent > 0: return f"+{percent:.1f}%"
        else: return f"{percent:.1f}%"

    # Convert image paths to absolute file URLs for embedding
    def img_path_to_url(rel_path):
        abs_path = os.path.abspath(rel_path)
        return f"file://{abs_path}"

    # Begin HTML
    html = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
                background: white;
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
                box-shadow: 0 0 5px #ddd;
                text-align: center;
            }}
            .metric-value {{
                font-size: 28px;
                font-weight: bold;
                margin-top: 10px;
            }}
            .metric-label {{
                font-size: 16px;
                color: #666;
            }}
            .weekly-metrics-table {{
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 40px;
            }}
            .weekly-metrics-table th, .weekly-metrics-table td {{
                border: 1px solid #ddd;
                padding: 10px;
                text-align: center;
            }}
            .weekly-metrics-table th {{
                background-color: #f0f8ff;
            }}
            .charts-section {{
                margin-bottom: 40px;
            }}
            .chart-img {{
                width: 600px;
                max-width: 100%;
                margin-bottom: 30px;
                border: 1px solid #ccc;
                border-radius: 8px;
                box-shadow: 0 0 10px #eee;
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
            .page-break {{
                page-break-after: always;
            }}
        </style>
    </head>
    <body>
        <h1>Content Performance Dashboard Report</h1>

        <h2>All-Time Summary Metrics (Facebook, X, Tik Tok only)</h2>
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
        <table class="weekly-metrics-table">
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

        <h2>Week-over-Week Performance by Platform</h2>
    """

    # Embed weekly trends images
    for platform in platforms:
        image_path = f"reports/images/{platform}_weekly_trends.png"
        if os.path.exists(image_path):
            image_url = img_path_to_url(image_path)
            html += f'<h3>{platform.title()} Views Over Time</h3>'
            html += f'<img class="chart-img" src="{image_url}">'

    # Embed platform comparison images
    platform_views_img = img_path_to_url("reports/images/platform_views.png")
    platform_likes_img = img_path_to_url("reports/images/platform_likes.png")
    alltime_views_img = img_path_to_url("reports/images/alltime_views.png")
    alltime_likes_img = img_path_to_url("reports/images/alltime_likes.png")
    top5_comparison_img = img_path_to_url("reports/images/top5_comparison.png")

    html += f"""
        <h2>Platform vs. Platform Comparison (Last 5 Weeks)</h2>
        <img class="chart-img" src="{platform_views_img}" alt="Platform Views">
        <img class="chart-img" src="{platform_likes_img}" alt="Platform Likes">

        <h2>All-Time Platform Comparison (Instagram Not Included)</h2>
        <img class="chart-img" src="{alltime_views_img}" alt="All Time Views">
        <img class="chart-img" src="{alltime_likes_img}" alt="All Time Likes">

        <div class="page-break"></div>

        <h2>Top 5 Posts Overview (Latest Week)</h2>
    """

    # Add Top 5 posts with links
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


    # Add Top 5 comparison image
    html += f"""
        <h2>Top 5 Posts Comparison (Latest 2 Weeks)</h2>
        <img class="chart-img" src="{top5_comparison_img}" alt="Top 5 Posts Comparison">
    </body>
    </html>
    """

    # Convert HTML to PDF
    HTML(string=html).write_pdf(output_path)
