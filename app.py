import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import date, timedelta

st.set_page_config(page_title="AI Trader Elite (2026 Upgrade)", layout="wide")

# Simple CSS injection to emulate a light/dark toggle (optional)
def inject_theme_css(dark: bool):
    if dark:
        css = """
        <style>
        .stApp { background-color: #0e1117; color: #e6eef8; }
        .css-1d391kg { color: #e6eef8; } /* headings (may vary by Streamlit versions) */
        </style>
        """
    else:
        css = """
        <style>
        .stApp { background-color: white; color: black; }
        </style>
        """
    st.markdown(css, unsafe_allow_html=True)

# Sidebar: inputs
st.sidebar.header("AI Trader Controls")
ticker = st.sidebar.text_input("Ticker", value="AAPL").upper()
days = st.sidebar.slider("Days of history", min_value=7, max_value=3650, value=365, step=1)
use_dark = st.sidebar.checkbox("Use dark theme (CSS injection)", value=False)
st.sidebar.markdown("---")
st.sidebar.markdown("Data source: yfinance (Yahoo Finance)")

# Apply theme CSS (optional)
inject_theme_css(use_dark)

# Data fetching with cache to avoid repeated downloads
@st.cache_data(ttl=3600)
def fetch_history(ticker_symbol: str, period_days: int) -> pd.DataFrame:
    end = date.today()
    start = end - timedelta(days=period_days)
    try:
        # yfinance download returns a DataFrame with a DatetimeIndex
        df = yf.download(ticker_symbol, start=start.isoformat(), end=end.isoformat(), progress=False)
    except Exception as e:
        st.error(f"Error fetching data for {ticker_symbol}: {e}")
        return pd.DataFrame()
    # Ensure index is datetime and columns exist
    if df.empty:
        return df
    df.index = pd.to_datetime(df.index)
    return df

st.title("AI Trader Elite — Market Viewer")
st.write("A minimal dashboard to preview historical price data. Extend this with your AI models, auth, and sheets integrations.")

if not ticker:
    st.warning("Enter a ticker symbol in the sidebar (e.g., AAPL, MSFT).")
else:
    with st.spinner(f"Fetching {ticker} data..."):
        df = fetch_history(ticker, days)

    if df is None or df.empty:
        st.error(f"No historical data found for ticker: {ticker}")
    else:
        # Summary metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Latest Close", f"${df['Close'].iloc[-1]:.2f}")
        col2.metric("Change (1d)", f"{(df['Close'].pct_change().iloc[-1]*100):.2f}%")
        col3.metric("Data Points", len(df))

        # Plot closing price
        st.subheader(f"{ticker} — Closing Price")
        st.line_chart(df['Close'])

        # Show a few rows and allow download
        st.subheader("Recent data")
        st.dataframe(df.tail(50))

        csv = df.to_csv().encode('utf-8')
        st.download_button(label="Download CSV", data=csv, file_name=f"{ticker}_history.csv", mime="text/csv")
