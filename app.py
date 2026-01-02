import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from alpha_vantage.timeseries import TimeSeries
from sklearn.linear_model import LinearRegression
from datetime import timedelta

# --- 1. CONFIG & SECRETS ---
try:
    API_KEY = st.secrets["AV_KEY"]
except:
    API_KEY = "MISSING"

st.set_page_config(page_title="AI TRADER ELITE v2026", layout="wide")

# Matrix-Terminal Style CSS
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    [data-testid="stMetricValue"] { color: #00FF41; font-family: 'monospace'; }
    .stTable { background-color: #111; border: 1px solid #00FF41; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA ENGINE ---
def get_clean_data(symbol):
    try:
        ts = TimeSeries(key=API_KEY, output_format='pandas')
        data, _ = ts.get_daily(symbol=symbol, outputsize='compact')
        # Cleanup column names
        data.columns = [c.split('. ')[1].capitalize() for c in data.columns]
        data.index = pd.to_datetime(data.index)
        return data.sort_index()
    except Exception as e:
        return pd.DataFrame()

# --- 3. AI FORECAST ENGINE ---
def run_ai_logic(df):
    # Train model on historical data
    X = np.arange(len(df)).reshape(-1, 1)
    y = df['Close'].values
    model = LinearRegression().fit(X, y)
    
    # Predict next 7 trading days
    future_indices = np.arange(len(df), len(df) + 7).reshape(-1, 1)
    predictions = model.predict(future_indices)
    
    # Create forecast
