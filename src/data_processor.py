# src/data_processor.py
import pandas as pd

def load_csv(file_path):
    """Load and validate the CSV file."""
    try:
        df = pd.read_csv(file_path)
        required_columns = ['week', 'platform', 'likes', 'views', 'follower_growth']
        if not all(col in df.columns for col in required_columns):
            raise ValueError("CSV missing required columns")
        # Convert 'week' to datetime, handle 'alltime' separately
        df['week'] = df['week'].apply(lambda x: pd.to_datetime(x, format='%Y-%m-%d') if x != 'alltime' else x)
        # Convert 'likes', 'views', 'follower_growth' to numeric, replacing 'n/a' with 0
        for col in ['likes', 'views', 'follower_growth']:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
        return df
    except Exception as e:
        raise Exception(f"Error loading CSV: {e}")

def get_summary_metrics(df, alltime=False):
    """Calculate total views, likes, and follower growth, optionally for alltime."""
    df_subset = df[df['week'] == 'alltime'] if alltime else df[df['week'] != 'alltime']
    return {
        'total_views': int(df_subset['views'].sum()),
        'total_likes': int(df_subset['likes'].sum()),
        'total_follower_growth': int(df_subset['follower_growth'].sum())
    }

def get_platform_breakdown(df):
    """Calculate views, likes, and follower growth by platform for non-alltime data."""
    return df[df['week'] != 'alltime'].groupby('platform')[['views', 'likes', 'follower_growth']].sum().reset_index()

def get_weekly_trends(df):
    """Calculate weekly views, likes, and follower growth trends for each platform."""
    trends = df[df['week'] != 'alltime'].groupby(['week', 'platform'])[['views', 'likes', 'follower_growth']].sum().reset_index()
    trends['week'] = trends['week'].dt.strftime('%Y-%m-%d')
    return trends

def get_top_platforms(df, n=5):
    """Get top N platforms by likes for the latest week."""
    latest_week = df[df['week'] != 'alltime']['week'].max()
    latest_df = df[df['week'] == latest_week]
    return latest_df[['week', 'platform', 'likes', 'views', 'follower_growth']].nlargest(n, 'likes')