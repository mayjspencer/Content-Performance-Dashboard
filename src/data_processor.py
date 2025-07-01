# src/data_processor.py
import pandas as pd

def load_csv(file_path):
    """Load and validate CSV file."""
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        raise Exception(f"Error loading CSV: {e}")

def process_data(df):
    """Process CSV data for dashboard."""
    return df