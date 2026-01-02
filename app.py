import streamlit as st
import yfinance as yf
import pandas as pd

# 1. FORCED MOBILE GLASS UI (2026 Chrome Hack)
st.set_page_config(page_title="Elite Trader ZAR", layout="wide")

st.markdown("""
<style>
    /* Fixed Background Gradient */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%) !important;
        background-attachment: fixed !important;
    }

    /* Brute-force removal of Streamlit's solid backgrounds */
    div[data-testid="stMetric"], .stSelectbox, .stTabs, .stSlider, .stInfo, .stSuccess, div[data-baseweb="input"] {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 18px !important;
        position: relative;
        overflow: hidden;
    }

    /* THE MAGIC: Pseudo-element blur for Mobile Chrome */
    div[data-testid="stMetric"]::before, .stSelectbox::before, .stTabs::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        backdrop-filter: blur(25px) saturate(180%);
        -webkit-backdrop-filter: blur(25px) saturate(180%);
        z-index: -1;
    }

    /* Text Clarity */
    h1, h2, h3, p, label, .stMetric label {
        color: white !important;
        font-family: 'Inter', sans-serif;
        text-shadow: 0px 2px 5px rgba(0,0,0,0.7);
    }
</style>
""", unsafe_allow_html=True)

# 2. THE SMART SEARCH (No Tickers Needed)
st.title("🛡️ Trader Command Center")

# A dictionary of the biggest companies for you
companies = {
    "Select a Company": "",
    "Absa Bank": "ABG.JO",
    "Sasol (Energy/Petrol)": "SOL.JO",
    "Naspers (Tech/Tencent)": "NPN.JO",
    "FirstRand (FNB)": "FSR.JO",
    "Capitec": "CPI.JO",
    "Apple (iPhone)": "AAPL",
    "Tesla (Elon Musk)": "TSLA",
    "S&P 500 (US Top 500)": "SPY"
}

# The Dropdown
selection = st.selectbox("Search for a Company", list(companies.keys()))
ticker = companies[selection]

if ticker:
    try:
        # Load Data
        df = yf.download(ticker, period="1y")
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
            
        # ZAR Exchange Rate
        fx = yf.download("USDZAR=X", period="1d")['Close'].iloc[-1]
        
        # Numbers
        price = float(df['Close'].iloc[-1])
        is_jse = ".JO" in ticker
        final_zar = price if is_jse else price * fx
        trend = df['Close'].rolling(200).mean().iloc[-1]

        # 3. THE DISPLAY
        st.subheader(f"Current Analysis: {selection}")
        
        m1, m2 = st.columns(2)
        m1.metric("Current Price (ZAR)", f"R{final_zar:,.2f}")
        m2.metric("USD/ZAR Rate", f"R{fx:.2f}")

        # The Chart
        st.area_chart(df['Close'])

        # 4. PLAIN ENGLISH GUIDANCE
        st.divider()
        if price > trend:
            st.success(f"🟢 BUY SIGNAL: {selection} is performing well. The trend is currently upward.")
        else:
            st.warning(f"🔴 CAUTION: {selection} is losing value. Professional advice would be to wait.")

    except:
        st.error("Market data unavailable for this selection.")

else:
    st.info("👋 Welcome. Please pick a company from the list above to see how they are performing today.")
