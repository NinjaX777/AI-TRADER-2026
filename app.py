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

# --- 2. THE GUNMETAL ANIMATED UI ---
# This CSS creates the illuminated cobalt look and animated gunmetal gradient
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    .stApp {
        background: linear-gradient(315deg, #1a1a1a 0%, #2c3e50 74%);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        color: #00d4ff;
        font-family: 'Orbitron', sans-serif;
    }

    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Neon Cobalt Text Illumination */
    h1, h2, h3, .stMetricValue {
        color: #00d4ff !important;
        text-shadow: 0 0 10px #00d4ff, 0 0 20px #00d4ff;
    }

    /* Custom Styling for Selectbox */
    div[data-baseweb="select"] {
        background-color: #2c3e50;
        border: 1px solid #00d4ff;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATA ENGINE ---
def get_clean_data(symbol):
    try:
        ts = TimeSeries(key=API_KEY, output_format='pandas')
        data, _ = ts.get_daily(symbol=symbol, outputsize='compact')
        data.columns = [c.split('. ')[1].capitalize() for c in data.columns]
        data.index = pd.to_datetime(data.index)
        return data.sort_index()
    except Exception as e:
        return pd.DataFrame()

# --- 4. MAIN INTERFACE ---
st.title("📟 AI TRADER ELITE")

# Dropdown with top tickers + Manual entry
top_tickers = ["AAPL", "TSLA", "NVDA", "BTC-USD", "ETH-USD", "MSFT", "AMZN", "META", "GOOGL", "NFLX"]
selected_ticker = st.selectbox("SELECT ASSET", options=top_tickers + ["OTHER..."])

if selected_ticker == "OTHER...":
    ticker = st.text_input("ENTER MANUAL SYMBOL").upper()
else:
    ticker = selected_ticker

if API_KEY == "MISSING":
    st.error("⚠️ Add AV_KEY to Secrets.")
elif ticker:
    df = get_clean_data(ticker)
    
    if not df.empty:
        # AI Forecast Logic
        X = np.arange(len(df)).reshape(-1, 1)
        y = df['Close'].values
        model = LinearRegression().fit(X, y)
        next_val = model.predict([[len(df)]])[0]
        
        # Metrics
        last = df['Close'].iloc[-1]
        c1, c2 = st.columns(2)
        c1.metric("CURRENT", f"${last:,.2f}")
        c2.metric("AI TARGET", f"${next_val:,.2f}", delta=f"{next_val-last:.2f}")

        # Plotly Candlestick with Cobalt Theme
        fig = go.Figure(data=[go.Candlestick(
            x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
            increasing_line_color='#00d4ff', decreasing_line_color='#ff0055'
        )])
        fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                          font=dict(family="Orbitron", color="#00d4ff"), xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No data found. Check symbol or API limits.")
