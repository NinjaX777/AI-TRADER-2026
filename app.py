import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from alpha_vantage.timeseries import TimeSeries
from sklearn.linear_model import LinearRegression
from datetime import timedelta

# --- 1. CONFIG ---
try:
    API_KEY = st.secrets["AV_KEY"]
except:
    API_KEY = "MISSING"

st.set_page_config(page_title="THE TRADER GEM", page_icon="💎", layout="wide")

# --- 2. THE BLACK GLASS & GOLD UI ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    /* 1. THE BACKGROUND: Force your design and kill all blue/purple gradients */
    .stApp {
        background-color: #000000 !important;
        background-image: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), 
                        url("https://i.ibb.co/vzYyS0N/Trader-Gem-BG.jpg"); /* REPLACE THIS URL WITH YOUR IMAGE LINK */
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
        font-family: 'Orbitron', sans-serif !important;
    }

    /* 2. THE BLACK GLASS PANE: High transparency frosted glass */
    div[data-testid="stVerticalBlock"] > div {
        background: rgba(0, 0, 0, 0.7) !important;
        backdrop-filter: blur(12px) !important;
        border: 2px solid #D4AF37 !important;
        border-radius: 15px !important;
        padding: 25px !important;
        box-shadow: 0 8px 32px 0 rgba(212, 175, 55, 0.2) !important;
    }

    /* 3. GOLD TEXT & ILLUMINATION: No more white or blue text */
    h1, h2, h3, p, label, .stMetricValue, [data-testid="stMetricLabel"] p {
        color: #D4AF37 !important;
        font-weight: 700 !important;
        text-shadow: 0 0 10px rgba(212, 175, 55, 0.8) !important;
    }

    /* 4. BUTTONS & INPUTS: Gold borders, Black backgrounds */
    div.stButton > button {
        background-color: #D4AF37 !important;
        color: #000000 !important;
        border: none !important;
        font-weight: bold !important;
        width: 100% !important;
    }

    input, div[data-baseweb="select"] {
        background-color: rgba(0, 0, 0, 0.9) !important;
        border: 1px solid #D4AF37 !important;
        color: #D4AF37 !important;
    }

    /* 5. CLEANUP: Hide Streamlit's default headers and footers */
    header, footer, #MainMenu {visibility: hidden !important;}
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
    except:
        return pd.DataFrame()

# --- 4. MAIN INTERFACE ---
st.markdown("<h1 style='text-align: center; font-size: 3.5rem;'>💎 THE TRADER GEM</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; letter-spacing: 10px; margin-bottom: 40px;'>PRECISION AI TRADING</p>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### ASSET SELECTION")
    top_tickers = ["AAPL", "TSLA", "NVDA", "BTC-USD", "ETH-USD", "MSFT", "AMZN", "META"]
    selected = st.selectbox("CHOOSE SYMBOL", options=top_tickers + ["OTHER"])
    
    ticker = selected
    if selected == "OTHER":
        ticker = st.text_input("ENTER CUSTOM", value="NVDA").upper()

if ticker:
    df = get_clean_data(ticker)
    
    if not df.empty:
        # AI Forecast Logic
        X = np.arange(len(df)).reshape(-1, 1)
        y = df['Close'].values
        model = LinearRegression().fit(X, y)
        last_price = df['Close'].iloc[-1]
        next_val = model.predict([[len(df)]])[0]
        
        with col2:
            # Metrics Row
            m1, m2, m3 = st.columns(3)
            m1.metric("CURRENT", f"${last_price:,.2f}")
            m2.metric("GEM TARGET", f"${next_val:,.2f}")
            m3.metric("STATUS", "ELITE" if next_val > last_price else "HOLD")

            # The Gold Candlestick Chart
            fig = go.Figure(data=[go.Candlestick(
                x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
                increasing_line_color='#D4AF37', decreasing_line_color='#444444',
                increasing_fillcolor='#D4AF37', decreasing_fillcolor='#444444'
            )])
            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color="#D4AF37", family="Orbitron"),
                xaxis_rangeslider_visible=False,
                margin=dict(t=0, b=0, l=0, r=0)
            )
            st.plotly_chart(fig, use_container_width=True)

            # Forecast Table
            st.markdown("### 🗓️ 5-DAY AI PROJECTION")
            future_idx = np.arange(len(df), len(df) + 5).reshape(-1, 1)
            preds = model.predict(future_idx)
            forecast_df = pd.DataFrame({
                'TIMEFRAME': [f"DAY {i}" for i in range(1, 6)],
                'PRICE TARGET': [f"${p:,.2f}" for p in preds]
            })
            st.table(forecast_df.set_index('TIMEFRAME'))
