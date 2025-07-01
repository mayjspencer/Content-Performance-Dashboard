# main.py
import streamlit as st
from src.dashboard import run_dashboard

if __name__ == "__main__":
    st.set_page_config(page_title="Content Performance Dashboard", layout="wide")
    run_dashboard()