import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from alpha_vantage.timeseries import TimeSeries
from sklearn.linear_model import LinearRegression

# --- 1. CONFIG & SYSTEM LOCK ---
# Fixed the parenthesis error here
st.set_page_config(page_title="THE TRADER GEM", page_icon="🟡", layout="wide")

# CSS NUCLEAR OPTION: Pure Gold & Black Glass. No Blue.
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Syncopate:wght@700&display=swap');
    
    /* THE BACKGROUND - Your hosted design */
    [data-testid="stAppViewContainer"] {
        background-color: #000000 !important;
        background-image: linear-gradient(rgba(0,0,0,0.65), rgba(0,0,0,0.65)), 
                        url("https://i.postimg.cc/85MscM8P/Trader-Gem-Final.jpg") !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }

    /* THE UNIQUE GEM LOGO - No Blue Diamonds */
    .logo-box { display: flex; justify-content: center; margin-top: 20px; }
    .gem-core {
        width: 60px; height: 60px; background: #D4AF37;
        clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
        box-shadow: 0 0 45px #D4AF37;
        animation: pulse-gem 3s infinite ease-in-out;
    }
    @keyframes pulse-gem {
        0%, 100% { transform: scale(1); filter: brightness(1); }
        50% { transform: scale(1.1); filter: brightness(1.4); box-shadow: 0 0 70px #D4AF37; }
    }

    /* THE BLACK GLASS PANE */
    .block-container {
        background: rgba(0, 0, 0, 0.85) !important;
        backdrop-filter: blur(25px) !important;
        border: 2px solid #D4AF37 !important;
        border-radius: 20px !important;
        padding: 50px !important;
        margin-top: 40px !important;
        box-shadow: 0 15px 50px rgba(0,0,0,0.8) !important;
    }

    /* TEXT LOCK */
    .main-title {
        font-family: 'Syncopate', sans-serif !important;
        color: #D4AF37 !important;
        text-align: center; font-size: 3.2rem; letter-spacing: 14px;
        margin-top: 15px; text-shadow: 0 0 25px rgba(212, 175, 55, 0.5);
    }
    h1, h2, h3, p, span, label, .stMetricValue {
        color: #D4AF37 !important;
        font-family: 'Orbitron', sans-serif !important;
    }

    /* UI CLEANUP - Kill Streamlit Blue Elements */
    header, footer { visibility: hidden !important; }
    div[data-baseweb="select"], input {
        background-color: #000 !important;
        border: 1px solid #D4AF37 !important;
        color: #D4AF37 !important;
    }
    
    /* Gold Buttons with Black Text */
    div.stButton > button {
        background-color: #D4AF37 !important;
        color: #000000 !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. HEADER ---
st.markdown('<div class="logo-box"><div class="gem-core"></div></div>', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">THE TRADER GEM</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #D4AF37; opacity: 0.8; letter-spacing: 6px;'>PRECISION AI INTERFACE</p>", unsafe_allow_html=True)

# --- 3. CORE LOGIC ---
col_side, col_main = st.columns([1, 2])

with col_side:
    st.subheader("ASSET SELECTION")
    ticker = st.selectbox("SYMBOL", ["NVDA", "BTC-USD", "AAPL", "TSLA", "ETH-USD"])
    if st.button("EXECUTE ANALYSIS"):
        st.success(f"ANALYZING {ticker}...")

if ticker:
    with col_main:
        m1, m2 = st.columns(2)
        # Display logic locked to gold
        m1.metric("CURRENT VALUE", "$286.25")
        m2.metric("GEM TARGET", "$312.40")

        # Gold Themed Chart
        fig = go.Figure(data=[go.Scatter(y=[280, 285, 282, 290, 286], 
                                         line=dict(color='#D4AF37', width=4))])
        fig.update_layout(template="plotly_dark", 
                          paper_bgcolor='rgba(0,0,0,0)', 
                          plot_bgcolor='rgba(0,0,0,0)', 
                          font=dict(color="#D4AF37", family="Orbitron"))
        st.plotly_chart(fig, use_container_width=True)
