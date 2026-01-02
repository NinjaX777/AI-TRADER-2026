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

st.set_page_config(page_title="THE TRADER GEM", page_icon="💎", layout="wide")

# --- 2. BLACK GLASS & GOLD UI ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    /* Background Image - Luxury Metal/Gold Theme */
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), 
                    url("https://images.unsplash.com/photo-1614850523296-d8c1af93d400?q=80&w=2070&auto=format&fit=crop");
        background-size: cover;
        background-attachment: fixed;
        font-family: 'Orbitron', sans-serif;
    }

    /* Black Glass Glassmorphism */
    .stMarkdown, .stDataFrame, .stTable, div[data-testid="stMetricValue"] {
        background: rgba(0, 0, 0, 0.6);
        backdrop-filter: blur(12px);
        border: 1px solid #D4AF37;
        padding: 15px;
        border-radius: 10px;
    }

    /* Logo and Header Styling */
    .main-title {
        color: #D4AF37;
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        text-shadow: 0 0 20px rgba(212, 175, 55, 0.6);
        margin-bottom: 0px;
    }

    .sub-logo {
        color: #D4AF37;
        text-align: center;
        font-size: 1rem;
        letter-spacing: 5px;
        margin-bottom: 30px;
    }

    /* Gold Accents & Bold Text */
    h1, h2, h3, label, [data-testid="stMetricLabel"] p {
        color: #D4AF37 !important;
        text-transform: uppercase;
    }

    .stMetricValue {
        color: #D4AF37 !important;
    }

    /* Gold Buttons / Black Text */
    div.stButton > button {
        background-color: #D4AF37 !important;
        color: #000000 !important;
        font-weight: bold;
        border-radius: 5px;
        border: none;
        transition: 0.3s;
    }
    
    div.stButton > button:hover {
        background-color: #FFD700 !important;
        box-shadow: 0 0 15px #D4AF37;
    }

    /* Input Fields */
    input, div[data-baseweb="select"] {
        background-color: rgba(0, 0, 0, 0.9) !important;
        border: 1px solid #D4AF37 !important;
        color: #D4AF37 !important;
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
    except:
        return pd.DataFrame()

# --- 4. MAIN INTERFACE ---
st.markdown('<p class="main-title">💎 THE TRADER GEM</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-logo">PRECISION AI TRADING</p>', unsafe_allow_html=True)

# Layout
col_side, col_main = st.columns([1, 3])

with col_side:
    st.subheader("Asset Selection")
    top_tickers = ["AAPL", "TSLA", "NVDA", "BTC-USD", "ETH-USD", "MSFT", "AMZN", "META"]
    selected = st.selectbox("Symbol Search", options=top_tickers + ["CUSTOM"])
    
    if selected == "CUSTOM":
        ticker = st.text_input("Enter Ticker", value="GOOGL").upper()
    else:
        ticker = selected

if ticker:
    df = get_clean_data(ticker)
    
    if not df.empty:
        # AI Forecast Logic
        X = np.arange(len(df)).reshape(-1, 1)
        y = df['Close'].values
        model = LinearRegression().fit(X, y)
        
        # Predictions
        last_price = df['Close'].iloc[-1]
        next_val = model.predict([[len(df)]])[0]
        
        with col_main:
            # Metrics
            m1, m2, m3 = st.columns(3)
            m1.metric("CURRENT", f"${last_price:,.2f}")
            m2.metric("AI PREDICTION", f"${next_val:,.2f}")
            m3.metric("STATUS", "ELITE" if next_val > last_price else "HOLD")

            # Chart
            fig = go.Figure(data=[go.Candlestick(
                x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
                increasing_line_color='#D4AF37', decreasing_line_color='#333333',
                increasing_fillcolor='#D4AF37', decreasing_fillcolor='#333333'
            )])
            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis_rangeslider_visible=False,
                margin=dict(t=0, b=0, l=0, r=0)
            )
            st.plotly_chart(fig, use_container_width=True)

            # Table
            st.subheader("Forecast Data")
            future_idx = np.arange(len(df), len(df) + 5).reshape(-1, 1)
            preds = model.predict(future_idx)
            forecast_df = pd.DataFrame({
                'Day': [f"T+{i}" for i in range(1, 6)],
                'Value': [f"${p:,.2f}" for p in preds]
            })
            st.table(forecast_df)
    else:
        st.error("Connection error. Check your API key or symbol.")
