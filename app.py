import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import date, timedelta

# 1. Page Configuration
st.set_page_config(page_title="AI Trader Elite (2026 Upgrade)", layout="wide", page_icon="📈")

# 2. Enhanced CSS Injection
def inject_theme_css(dark: bool):
    if dark:
        css = """
        <style>
        .stApp { background-color: #0e1117; color: #e6eef8; }
        [data-testid="stMetricValue"] { color: #00ffcc; }
        </style>
        """
    else:
        css = """
        <style>
        .stApp { background-color: #ffffff; color: #000000; }
        </style>
        """
    st.markdown(css, unsafe_allow_html=True)

# 3. Sidebar Controls
st.sidebar.header("🕹️ AI Trader Controls")
ticker = st.sidebar.text_input("Ticker Symbol", value="AAPL").upper()
days = st.sidebar.slider("Days of history", min_value=7, max_value=3650, value=365, step=1)
use_dark = st.sidebar.checkbox("Use custom dark theme", value=True)
st.sidebar.markdown("---")

inject_theme_css(use_dark)

# 4. Robust Data Fetching
@st.cache_data(ttl=3600)
def fetch_history(ticker_symbol: str, period_days: int) -> pd.DataFrame:
    end = date.today()
    start = end - timedelta(days=period_days)
    try:
        # Fetch data
        df = yf.download(ticker_symbol, start=start, end=end, progress=False)
        
        if df.empty:
            return pd.DataFrame()

        # FIX: Flatten Multi-index columns if they exist
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
            
        df.index = pd.to_datetime(df.index)
        return df
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

# 5. Main UI Logic
st.title("📈 AI Trader Elite — Market Viewer")
st.caption("2026 Edition | Real-time Market Data & Analytics")

if not ticker:
    st.warning("Please enter a ticker symbol to begin.")
else:
    with st.spinner(f"Analyzing {ticker}..."):
        df = fetch_history(ticker, days)

    if df.empty:
        st.error(f"No data found for '{ticker}'. Please check the symbol and try again.")
    else:
        # Metrics Calculation
        last_close = float(df['Close'].iloc[-1])
        prev_close = float(df['Close'].iloc[-2])
        change = ((last_close - prev_close) / prev_close) * 100

        # Layout: Metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Latest Close", f"${last_close:,.2f}")
        m2.metric("Daily Change", f"{change:.2f}%", delta=f"{change:.2f}%")
        m3.metric("Data Points", len(df))

        # Layout: Chart
        st.subheader(f"Price Action: {ticker}")
        st.line_chart(df['Close'], use_container_width=True)

        # Layout: Data Table & Export
        with st.expander("View Raw Data Records"):
            st.dataframe(df.sort_index(ascending=False), use_container_width=True)
            
            csv = df.to_csv().encode('utf-8')
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"{ticker}_history.csv",
                mime="text/csv"
            )

st.sidebar.info("Tip: Use the slider to adjust the lookback period for technical analysis.")
