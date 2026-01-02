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

# Set page title and a custom gold icon
st.set_page_config(page_title="THE TRADER GEM", page_icon="🟡", layout="wide")

# --- 2. THE TOTAL DESIGN OVERHAUL (ZERO BLUE) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Syncopate:wght@700&display=swap');
    
    /* KILL ALL DEFAULT STREAMLIT THEMING */
    [data-testid="stAppViewContainer"] {
        background-color: #000000 !important;
        background-image: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
                        url("https://i.ibb.co/vzYyS0N/Trader-Gem-BG.jpg") !important;
        background-size: cover !important;
        background-attachment: fixed !important;
    }

    /* THE TRADER GEM UNIQUE LOGO - Custom CSS Design */
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 10px;
    }
    .gem-logo {
        width: 60px;
        height: 60px;
        background: #D4AF37;
        clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
        box-shadow: 0 0 30px #D4AF37;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); opacity: 0.8; }
        50% { transform: scale(1.1); opacity: 1; box-shadow: 0 0 50px #D4AF37; }
        100% { transform: scale(1); opacity: 0.8; }
    }

    /* GLASSMORPHISM - Black Glass Pane */
    .block-container {
        background: rgba(0, 0, 0, 0.8) !important;
        backdrop-filter: blur(25px) !important;
        border: 2px solid #D4AF37 !important;
        border-radius: 20px !important;
        padding: 40px !important;
        margin-top: 50px !important;
    }

    /* PURE GOLD TEXT */
    h1, h2, h3, p, span, label, .stMetricValue {
        color: #D4AF37 !important;
        font-family: 'Orbitron', sans-serif !important;
        text-shadow: 0 0 15px rgba(212, 175, 55, 0.5) !important;
    }
    
    .main-title {
        font-family: 'Syncopate', sans-serif !important;
        font-size: 3.5rem !important;
        text-align: center;
        letter-spacing: 15px !important;
        color: #D4AF37 !important;
    }

    /* INPUTS & BUTTONS */
    div[data-baseweb="select"], input {
        background-color: #000 !important;
        border: 1px solid #D4AF37 !important;
        color: #D4AF37 !important;
    }
    
    button {
        background-color: #D4AF37 !important;
        color: #000 !important;
        font-weight: bold !important;
    }

    /* CLEANUP */
    header, footer {visibility: hidden !important;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. THE TRADER GEM LOGO & HEADER ---
st.markdown('<div class="logo-container"><div class="gem-logo"></div></div>', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">THE TRADER GEM</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; letter-spacing: 5px; opacity: 0.7;'>V 2 0 2 6 . E L I T E</p>", unsafe_allow_html=True)

# --- 4. DATA ENGINE ---
def get_data(symbol):
    try:
        ts = TimeSeries(key=API_KEY, output_format='pandas')
        data, _ = ts.get_daily(symbol=symbol, outputsize='compact')
        data.columns = [c.split('. ')[1].capitalize() for c in data.columns]
        return data.sort_index()
    except:
        return pd.DataFrame()

# --- 5. INTERFACE ---
c_left, c_right = st.columns([1, 2])

with c_left:
    st.subheader("SYSTEM ACCESS")
    ticker = st.selectbox("CHOOSE ASSET", ["NVDA", "TSLA", "AAPL", "BTC-USD", "ETH-USD"])

if ticker:
    df = get_data(ticker)
    if not df.empty:
        # AI Logic
        X = np.arange(len(df)).reshape(-1, 1)
        y = df['Close'].values
        model = LinearRegression().fit(X, y)
        next_p = model.predict([[len(df)]])[0]
        
        with c_right:
            col_m1, col_m2 = st.columns(2)
            col_m1.metric("CURRENT", f"${df['Close'].iloc[-1]:,.2f}")
            col_m2.metric("GEM TARGET", f"${next_p:,.2f}")

            # Plotly Chart
            fig = go.Figure(data=[go.Candlestick(
                x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
                increasing_line_color='#D4AF37', decreasing_line_color='#333',
                increasing_fillcolor='#D4AF37', decreasing_fillcolor='#333'
            )])
            fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', 
                              plot_bgcolor='rgba(0,0,0,0)', xaxis_rangeslider_visible=False,
                              font=dict(color="#D4AF37", family="Orbitron"))
            st.plotly_chart(fig, use_container_width=True)
