# Content Performance Dashboard

A local Streamlit dashboard for analyzing social media performance from CSV data.

## Overview
Visualizes metrics (views, reach, posts) across platforms, compares weekly performance, and generates PDF reports. Runs locally for privacy.

## Setup
1. Clone the repo: `git clone <repo-url>`
2. Create virtual environment: `python3 -m venv venv`
3. Activate: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run: `streamlit run main.py`

## Sample Data
- `data/sample/sample_data.csv`: Dummy data for testing.

## Structure
- `data/input/`: Private CSV uploads (not tracked).
- `data/sample/`: Public dummy data.
- `src/`: Core Python modules.
- `reports/`: Generated reports (not tracked).