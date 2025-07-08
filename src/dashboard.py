# src/dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
from src.data_processor import load_csv, get_summary_metrics, get_platform_breakdown, get_weekly_trends, get_top_platforms
import os

def run_dashboard():
    st.title("Content Performance Dashboard")
    st.write("Analyze week-over-week social media performance by platform.")

    # File grab
    input_dir = "data/input"
    data_file_path = os.path.join(input_dir, "socialmedia.csv")
    
    try:
        df = load_csv(data_file_path)
        
        # All-Time Summary Metrics
        st.subheader("All-Time Summary Metrics (Facebook, X, and Tik Tok only)")
        alltime_metrics = get_summary_metrics(df, alltime=True)
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Views (All-Time)", f"{alltime_metrics['total_views']:,}")
        col2.metric("Total Likes (All-Time)", f"{alltime_metrics['total_likes']:,}")
        col3.metric("Total Follower Growth (All-Time)", f"{alltime_metrics['total_follower_growth']:,}")

        # Weekly Summary Comparison
        st.subheader("Weekly Summary Metrics (Latest Week: 2025-06-25)")

        # Only work with rows AFTER the alltime block (skip first 4 rows)
        df_weekly = df.iloc[4:].reset_index(drop=True)

        col1, col2, col3 = st.columns(3)

        # Assume platforms appear in the same order every 4 rows (Instagram, Facebook, TikTok, X)
        platforms = df_weekly['platform'].unique()

        for i, platform in enumerate(platforms):
            row = i  # latest week's row for this platform
            compare_row = row + 4  # the same platform, previous week

            # Make sure we have enough data to compare
            if compare_row >= len(df_weekly):
                continue

            current_row = df_weekly.iloc[row]
            previous_row = df_weekly.iloc[compare_row]

            # Safety check: ensure same platform
            if current_row['platform'] != previous_row['platform']:
                continue

            current_views = int(current_row['views'])
            current_likes = int(current_row['likes'])
            current_followers = int(current_row['follower_growth'])

            prev_views = int(previous_row['views'])
            prev_likes = int(previous_row['likes'])
            prev_followers = int(previous_row['follower_growth'])

            def calc_percent_change(current, previous):
                if previous == 0:
                    return float('inf') if current != 0 else 0
                return ((current - previous) / previous) * 100

            def format_percent(percent):
                if percent == float('inf'):
                    return "+∞%"
                elif percent == 0:
                    return "0%"
                elif percent > 0:
                    return f"+{percent:.1f}%"
                else:
                    return f"{percent:.1f}%"

            views_percent = calc_percent_change(current_views, prev_views)
            likes_percent = calc_percent_change(current_likes, prev_likes)
            followers_percent = calc_percent_change(current_followers, prev_followers)

            with col1:
                st.metric(f"{platform} Views", f"{current_views:,}", delta=format_percent(views_percent), delta_color="normal")
            with col2:
                st.metric(f"{platform} Likes", f"{current_likes:,}", delta=format_percent(likes_percent), delta_color="normal")
            with col3:
                st.metric(f"{platform} Follower Growth", f"{current_followers:,}", delta=format_percent(followers_percent), delta_color="normal")

        # Week-over-Week Trends by Platform
        st.subheader("Week-over-Week Performance by Platform")
        # Metric selector
        metric = st.selectbox("Select Metric to Compare", options=["views", "likes", "follower_growth"],
                                format_func=lambda x: x.replace("_", " ").title())
        trends_data = get_weekly_trends(df)
        platforms = trends_data['platform'].unique()
        for platform in platforms:
            platform_data = trends_data[trends_data['platform'] == platform]
            fig = px.bar(platform_data, x='week', y=metric,
                            title=f"Week-over-Week {metric.replace('_', ' ').title()}: {platform}",
                            labels={metric: metric.replace("_", " ").title(), 'week': 'Week'},
                            color='platform')
            st.plotly_chart(fig, use_container_width=True)
        
        # Platform vs. Platform Comparison
        st.subheader("Platform vs. Platform Comparison (Last 5 Weeks)")
        platform_data = get_platform_breakdown(df)
        fig_views = px.bar(platform_data, x='platform', y='views', title="Total Views by Platform",
                            color='platform')
        fig_likes = px.bar(platform_data, x='platform', y='likes', title="Total Likes by Platform",
                            color='platform')
        col1, col2 = st.columns(2)
        col1.plotly_chart(fig_views, use_container_width=True)
        col2.plotly_chart(fig_likes, use_container_width=True)

        # All-Time Platform Comparison
        st.subheader("All-Time Platform Comparison (Instagram Not Included)")
        alltime_data = df[df['week'] == 'alltime'].groupby('platform')[['views', 'likes', 'follower_growth']].sum().reset_index()
        fig_views_alltime = px.bar(alltime_data, x='platform', y='views', title="All-Time Total Views by Platform",
                                color='platform')
        fig_likes_alltime = px.bar(alltime_data, x='platform', y='likes', title="All-Time Total Likes by Platform",
                                color='platform')
        col1, col2 = st.columns(2)
        col1.plotly_chart(fig_views_alltime, use_container_width=True)
        col2.plotly_chart(fig_likes_alltime, use_container_width=True)
            
    except Exception as e:
        st.error(f"Error: {e}")