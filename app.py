import streamlit as st
import yfinance as yf
import pandas as pd

# 1. PROFESSIONAL GLASS UI ENGINE (Optimized for 2026 Mobile Chrome)
st.set_page_config(page_title="AI Trader Elite", layout="wide")

# CSS designed for high performance and visual depth on mobile
st.markdown("""
<style>
    /* Background: Deep vibrant gradient for maximum glass contrast */
    .stApp {
        background: linear-gradient(145deg, #0b0d17 0%, #1c2341 50%, #111421 100%) !important;
        background-attachment: fixed !important;
    }

    /* Target the Mobile Glass panels with absolute precision */
    [data-testid="stMetric"], .stSelectbox, .stTabs, div[data-baseweb="input"], .stAlert {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(25px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(25px) saturate(180%) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 24px !important;
        padding: 18px !important;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4) !important;
    }

    /* Fixed white typography for legibility on small screens */
    h1, h2, h3, p, label, .stMetric label {
        color: #ffffff !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        text-shadow: 0px 2px 4px rgba(0,0,0,0.8);
    }

    /* Transparent Sidebar for sleek navigation */
    [data-testid="stSidebar"] {
        background-color: rgba(10, 10, 20, 0.6) !important;
        backdrop-filter: blur(15px) !important;
    }
</style>
""", unsafe_allow_html=True)

# 2. PRO DATA LOGIC (Cat-and-Mouse yfinance fix)
@st.cache_data(ttl=3600)
def fetch_pro_data(ticker):
    try:
        # Requesting data with auto_adjust to bypass structural errors
        df = yf.download(ticker, period="1y", interval="1d", auto_adjust=True)
        if df.empty: return None, 18.50
        
        # Flatten MultiIndex if necessary
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # Get the ZAR exchange rate safely
        fx_df = yf.download("USDZAR=X", period="1d")
        fx = fx_df['Close'].iloc[-1] if not fx_df.empty else 18.50
        
        return df, float(fx)
    except:
        return None, 18.50

# 3. MINIMALIST DASHBOARD
st.title("🛡️ Trader Command")

# Simplified search options (Professional curated list)
pro_list = {
    "Select Entity": "",
    "Absa Bank": "ABG.JO",
    "Sasol Limited": "SOL.JO",
    "Naspers (Tech)": "NPN.JO",
    "FirstRand Ltd": "FSR.JO",
    "Apple Inc.": "AAPL",
    "Tesla Inc.": "TSLA",
    "S&P 500 Index": "SPY"
}

selection = st.selectbox("Search Market:", list(pro_list.keys()))
ticker = pro_list[selection]

if ticker:
    data, zar_rate = fetch_pro_data(ticker)
    
    if data is not None:
        curr_p = float(data['Close'].iloc[-1])
        is_jse = ".JO" in ticker
        price_zar = curr_p if is_jse else curr_p * zar_rate
        
        # Pro Performance Row
        m1, m2 = st.columns(2)
        m1.metric("Live Price", f"R{price_zar:,.2f}")
        m2.metric("Exchange Rate", f"R{zar_rate:.2f}")

        # Area chart for that high-end "Pro" feel
        st.area_chart(data['Close'])

        # Final Strategy Output
        st.divider()
        ma200 = data['Close'].rolling(200).mean().iloc[-1]
        if curr_p > ma200:
            st.success(f"🟢 {selection} is in a LONG-TERM GROWTH phase.")
        else:
            st.warning(f"🔴 {selection} is currently under-performing the 200-day average.")
    else:
        st.error("Market feed interrupted. Please pick another option.")
else:
    st.info("Tap 'Search Market' above to begin.")
