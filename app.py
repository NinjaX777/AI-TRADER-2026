import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from alpha_vantage.timeseries import TimeSeries
from sklearn.linear_model import LinearRegression

# --- 1. CONFIG & SYSTEM LOCK ---
st.set_page_config(page_title="THE TRADER GEM", page_icon="🟡", layout="wide")

# CSS NUCLEAR OPTION: Purges blue, forces glass, and locks your hosted background
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Syncopate:wght@700&display=swap');
    
    /* THE BACKGROUND - Permanent Direct Link to your Design */
    [data-testid="stAppViewContainer"] {
        background-color: #000000 !important;
        background-image: linear-gradient(rgba(0,0,0,0.65), rgba(0,0,0,0.65)), 
                        url("https://i.postimg.cc/85MscM8P/Trader-Gem-Final.jpg") !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }

    /* THE GEM LOGO - Unique, Modern, No Emojis */
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

    /* THE BLACK GLASS PANE - High Blur, Pure Gold Borders */
    .block-container {
        background: rgba(0, 0, 0, 0.85) !important;
        backdrop-filter: blur(25px) !important;
        border: 2px solid #D4AF37 !important;
        border-radius: 20px !important;
        padding: 50px !important;
        margin-top: 40px !important;
        box-shadow: 0 15px 50px rgba(0,0,0,0.8) !important;
    }

    /* TYPOGRAPHY LOCK */
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

    /* UI CLEANUP */
    header, footer { visibility: hidden !important; }
    div[data-baseweb="select"], input {
        background-color: #000 !important;
        border: 1px solid #D4AF37 !important;
        color: #D4AF37 !important;
    }
    </style>
    """, unsafe_allow_html=
