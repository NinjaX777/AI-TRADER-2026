import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

# Use modern design with light/dark theme switch functionality
st.set_page_config(page_title="AI Trader Elite (2026 Upgrade)", layout="wide")


# Dynamically apply styles based on the theme
def bring_styles(theme_pref):
    if theme_pref == "dark":
        return """
        <style>
            .stApp {
                background: linear-gradient(145deg, #0b0d17 0%, #1c2341 50%, #111421 100%) !important;
                background-attachment: fixed !important;
            }
            .stMetric, .stSelectbox, .stTabs, div[data-baseweb="input"], .stAlert {
                background: rgba(255, 255, 255, 0.05) !important;
                backdrop-filter: blur(20px) saturate(150%) !important;
                color: #ffffff !important;
                border: 1px solid rgba(255, 255, 255, 0.2) !important;
                border-radius: 16px !important;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5) !important;
            }
            h1, h2, h3, p, label, .stMetric label {
                color: #ffffff !important;
                text-shadow: 0px 2px 4px rgba(0, 0, 0, 0.6);
            }
        </style>
        """
    elif theme_pref == "light":
        return """
        <style>
            .stApp {
                background: white !important;
                color: black !important;
            }
            .stMetric, .stSelectbox, .stTabs, div[data-baseweb="input"], .stAlert {
                background: rgba(0, 0, 0, 0.05) !important;
                backdrop-filter: blur(10px) saturate(120%) !important;
                color: #000000 !important;
                border: 1px solid rgba(0, 0, 0, 0.1) !important;
                border-radius: 16px !important;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2) !important;
            }
            h1, h2, h3, p, label, .stMetric label {
                color: #000000 !important;
            }
        </style>
        """

# Add a theme selector in the sidebar
selected_theme = st.sidebar.radio("Select Theme:", ["dark", "light"], index=0)
st.markdown(bring_styles(selected_theme), unsafe_allow_html=True)

# Caching the financial data to improve performance
@st.cache_data(ttl=3600)
def fetch_pro_data(ticker):
    try:
        data = yf.download(ticker, period="1y", interval="1d", auto_adjust=True)
        if data.empty:
            return None, 18.50

        # Flatten MultiIndex if necessary
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        # Fetch USD to ZAR exchange rate
        fx_data = yf.download("USDZAR=X", period="1d")
        fx = fx_data["Close"].iloc[-1] if not fx_data.empty else 18.50

        return data, float(fx)
    except Exception as e:
        return None, 18.50


# Set title and styling for the application's main page
st.title("🛡️ AI Trader Elite Dashboard")

# Dropdown menu for selecting market entities
market_list = {
    "Select an entity": "",
    "Absa Bank": "ABG.JO",
    "Sasol Limited": "SOL.JO",
    "Naspers": "NPN.JO",
    "FirstRand Ltd": "FSR.JO",
    "Apple Inc.": "AAPL",
    "Tesla Inc.": "TSLA",
    "S&P 500 Index": "SPY"
}

chosen_entity = st.selectbox("Choose a market:", list(market_list.keys()))
symbol = market_list[chosen_entity]

# Display market data and charts once an entity is selected
if symbol:
    stock_data, zar_rate = fetch_pro_data(symbol)

    if stock_data is not None:
        current_price = float(stock_data['Close'].iloc[-1])
        is_jse_ticker = '.JO' in symbol
        price_in_zar = current_price if is_jse_ticker else current_price * zar_rate

        # Dynamic data metrics
        col1, col2 = st.columns(2)
        col1.metric("Live Price", f"R {price_in_zar:,.2f}")
        col2.metric("Exchange Rate (USDZAR)", f"R {zar_rate:.2f}")

        # Financial chart for high-end visualization
        st.area_chart(stock_data['Close'])

        # Add a strategy output section
        moving_avg_200 = stock_data['Close'].rolling(200).mean().iloc[-1]
        st.divider()

        if current_price > moving_avg_200:
            st.success(f"🟢 {chosen_entity} is currently in a bullish phase.")
        else:
            st.warning(f"🔴 {chosen_entity} is currently below the 200-day moving average.")
    else:
        st.error("Failed to fetch market data. Please try again.")
else:
    st.info("Use the dropdown above to select a market.")
