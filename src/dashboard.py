import streamlit as st
import pandas as pd
import plotly.express as px
from src.data_processor import (
    load_socialmedia_csv, load_top5_csv,
    get_summary_metrics, get_platform_breakdown,
    get_weekly_trends, get_top_platforms
)
import os

def run_dashboard():
    st.title("Content Performance Dashboard")
    st.write("Analyze week-over-week social media performance by platform.")

    input_dir = "data/input"
    socialmedia_path = os.path.join(input_dir, "socialmedia.csv")
    top5_path = os.path.join(input_dir, "top5.csv")
    
    try:
        social_df = load_socialmedia_csv(socialmedia_path)
        top5_df = load_top5_csv(top5_path)

        # All-Time Summary Metrics
        st.subheader("All-Time Summary Metrics (Facebook, X, and Tik Tok only)")
        alltime_metrics = get_summary_metrics(social_df, alltime=True)
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Views (All-Time)", f"{alltime_metrics['total_views']:,}")
        col2.metric("Total Likes (All-Time)", f"{alltime_metrics['total_likes']:,}")
        col3.metric("Total Follower Growth (All-Time)", f"{alltime_metrics['total_follower_growth']:,}")

        # Weekly Summary Comparison
        st.subheader("Weekly Summary Metrics (Latest Week)")
        df_weekly = social_df.iloc[4:].reset_index(drop=True)
        col1, col2, col3 = st.columns(3)
        platforms = df_weekly['platform'].unique()

        for i, platform in enumerate(platforms):
            row = i
            compare_row = row + 4
            if compare_row >= len(df_weekly): continue

            current_row = df_weekly.iloc[row]
            previous_row = df_weekly.iloc[compare_row]
            if current_row['platform'] != previous_row['platform']: continue

            current_views = int(current_row['views'])
            current_likes = int(current_row['likes'])
            current_followers = int(current_row['follower_growth'])
            prev_views = int(previous_row['views'])
            prev_likes = int(previous_row['likes'])
            prev_followers = int(previous_row['follower_growth'])

            def calc_percent_change(current, previous):
                if previous == 0: return float('inf') if current != 0 else 0
                return ((current - previous) / previous) * 100

            def format_percent(percent):
                if percent == float('inf'): return "+∞%"
                elif percent == 0: return "0%"
                elif percent > 0: return f"+{percent:.1f}%"
                else: return f"{percent:.1f}%"

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
        metric = st.selectbox("Select Metric to Compare", options=["views", "likes", "follower_growth"],
                                format_func=lambda x: x.replace("_", " ").title())
        trends_data = get_weekly_trends(social_df)
        platforms = trends_data['platform'].unique()
        for platform in platforms:
            platform_data = trends_data[trends_data['platform'] == platform]
            fig = px.bar(platform_data, x='week', y=metric,
                         title=f"{metric.replace('_', ' ').title()} on {platform}",
                         labels={metric: metric.replace("_", " ").title(), 'week': 'Week'},
                         color='platform')
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        # Platform vs. Platform Comparison
        st.subheader("Platform vs. Platform Comparison (Last 5 Weeks)")
        platform_data = get_platform_breakdown(social_df)
        fig_views = px.bar(platform_data, x='platform', y='views', title="Total Views", color='platform')
        fig_likes = px.bar(platform_data, x='platform', y='likes', title="Total Likes", color='platform')
        fig_views.update_layout(showlegend=False)
        fig_likes.update_layout(showlegend=False)
        col1, col2 = st.columns(2)
        col1.plotly_chart(fig_views, use_container_width=True)
        col2.plotly_chart(fig_likes, use_container_width=True)

        # All-Time Platform Comparison
        st.subheader("All-Time Platform Comparison (Instagram Not Included)")
        alltime_data = social_df[social_df['week'] == 'alltime'].groupby('platform')[['views', 'likes', 'follower_growth']].sum().reset_index()
        fig_views_alltime = px.bar(alltime_data, x='platform', y='views', title="All-Time Views", color='platform')
        fig_likes_alltime = px.bar(alltime_data, x='platform', y='likes', title="All-Time Likes", color='platform')
        fig_views_alltime.update_layout(showlegend=False)
        fig_likes_alltime.update_layout(showlegend=False)
        col1, col2 = st.columns(2)
        col1.plotly_chart(fig_views_alltime, use_container_width=True)
        col2.plotly_chart(fig_likes_alltime, use_container_width=True)

        # Top 5 Table
        st.subheader("Top 5 Posts Overview (Latest Week)")
        top5_recent = top5_df.tail(5).copy()
        top5_recent['Label'] = [f"{i+1}. {pt}" for i, pt in enumerate(top5_recent['Post Type'])]

        for i, row in top5_recent.iterrows():
            views = f"{row['Views']:,}"
            engagement = f"{row['Engagement']:,}"
            link = row['Link']
            post_type = row['Post Type']
            
            st.markdown(
                f"""
                <div style="border: 1px solid #ddd; border-radius: 8px; padding: 12px; margin-bottom: 10px; background-color: #f9f9f9;">
                    <strong>{i - top5_recent.index[0] + 1}. {post_type}</strong><br>
                    <a href="{link}" target="_blank" style="color: #1f77b4; text-decoration: none;">View Post 🔗</a><br>
                    <strong>{views} views • {engagement} engagement</strong>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Top 5 Comparison
        st.subheader("Top 5 Posts Comparison (Latest 2 Weeks)")
        latest_top5 = top5_df.tail(5).copy().reset_index(drop=True)
        previous_top5 = top5_df.tail(10).head(5).copy().reset_index(drop=True)
        latest_top5['Week'] = 'This Week'
        previous_top5['Week'] = 'Last Week'
        latest_top5['Rank'] = [f"Post {i+1}" for i in range(5)]
        previous_top5['Rank'] = [f"Post {i+1}" for i in range(5)]
        combined_top5 = pd.concat([latest_top5, previous_top5], ignore_index=True)

        fig_top5_compare = px.bar(
            combined_top5,
            x='Rank',
            y='Views',
            color='Week',
            barmode='group',
            text='Views',
            labels={'Views': 'Views', 'Rank': 'Post Rank', 'Week': 'Week'},
            color_discrete_map={'This Week': '#1f77b4', 'Last Week': '#000000'},
        )

        fig_top5_compare.update_traces(texttemplate='%{text:,}', textposition='outside')
        fig_top5_compare.update_layout(
            showlegend=False,
            xaxis_title='Post Rank',
            yaxis_title='Views'
        )

        st.plotly_chart(fig_top5_compare, use_container_width=True)

    except Exception as e:
        st.error(f"Error: {e}")
