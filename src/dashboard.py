# src/dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
from src.data_processor import load_csv, get_summary_metrics, get_platform_breakdown, get_weekly_trends, get_top_platforms

def run_dashboard():
    st.title("Content Performance Dashboard")
    st.write("Analyze week-over-week social media performance by platform.")

    # File uploader
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file:
        try:
            df = load_csv(uploaded_file)
            
            # All-Time Summary Metrics
            st.subheader("All-Time Summary Metrics")
            alltime_metrics = get_summary_metrics(df, alltime=True)
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Views (All-Time)", f"{alltime_metrics['total_views']:,}")
            col2.metric("Total Likes (All-Time)", f"{alltime_metrics['total_likes']:,}")
            col3.metric("Total Follower Growth (All-Time)", f"{alltime_metrics['total_follower_growth']:,}")
            
            # Weekly Summary Metrics
            st.subheader("Weekly Summary Metrics (Latest Week: 2025-06-25)")
            latest_week = df[df['week'] != 'alltime']['week'].max()
            latest_df = df[df['week'] == latest_week]
            platforms = latest_df['platform'].unique()
            col1, col2, col3 = st.columns(3)
            for platform in platforms:
                platform_data = latest_df[latest_df['platform'] == platform]
                with col1:
                    st.metric(f"{platform} Views", f"{int(platform_data['views'].sum()):,}")
                with col2:
                    st.metric(f"{platform} Likes", f"{int(platform_data['likes'].sum()):,}")
                with col3:
                    st.metric(f"{platform} Follower Growth", f"{int(platform_data['follower_growth'].sum()):,}")
        
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
            
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.info("Please upload a CSV file to begin.")