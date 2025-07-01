# src/dashboard.py
import streamlit as st
import pandas as pd

def run_dashboard():
    st.title("Content Performance Dashboard")
    st.write("Welcome to the dashboard! Upload a CSV to get started.")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write("Data Preview:")
        st.dataframe(df.head())