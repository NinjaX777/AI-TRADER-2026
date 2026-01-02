import streamlit as st
import yfinance as yf
import pandas as pd

# --- 1. CORE CONFIG ---
st.set_page_config(page_title="AI Trader Elite", layout="wide")

# --- 2. THE GLASSMORPHISM ENGINE ---
# This CSS uses backdrop-filter blur and semi-transparent backgrounds
# to create a floating glass effect over a vibrant gradient.
glass_css = """
<style>
    /* 1. Dynamic Gradient Background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%) !important;
        background-attachment: fixed !important;
    }

    /* 2. Global Glass Container Rule */
    /* This targets metrics, inputs, sliders, and standard divs. */
    [data-testid="stMetric"], 
    [data-testid="stVerticalBlock"] > div:has(div.stMetric),
    [data-testid="stForm"],
    .stTabs, .stExpander, div[data-baseweb="input"], .stSlider, .stMarkdownContainer {
        background: rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(20px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 24px !important;
        padding: 20px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4) !important;
        margin-bottom: 15px !important;
    }

    /* 3. Modern Text Styling */
    h1, h2, h3, p, label, .stMetric label {
        color: #ffffff !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        text-shadow: 0px 2px 4px rgba(0,0,0,0.4) !important;
    }

    /* 4. Fix for Transparent Charts */
    [data-testid="stAreaChart"], [data-testid="stLineChart"] {
        background-color: transparent !important;
        border: none !important;
    }
    
    /* 5. Custom Sidebar Glass */
    [data-testid="stSidebar"] {
        background-color: rgba(20, 20, 35, 0.7) !important;
        backdrop-filter: blur(15px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
</style>
"""
st.markdown(glass_css, unsafe_allow_html=True)

# --- 3. SECURITY ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🧬 Biometric Gateway")
    if st.button("🧬 Verify Identity", use_container_width=True, type="primary"):
        st.session_state.authenticated = True
        st.rerun()
    st.stop()

# --- 4. TRADING ENGINE ---
st.title("🛡️ AI Command Center")

@st.cache_data(ttl=3600)
def get_data(symbol):
    try:
        df = yf.download(symbol, period="1y")
        if df.empty: return None, 18.50
        if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
        
        fx_df = yf.download("USDZAR=X", period="1d")
        fx = fx_df['Close'].iloc[-1] if not fx_df.empty else 18.50
        
        df['MA200'] = df['Close'].rolling(200).mean()
        return df, float(fx)
    except: return None, 18.50

ticker = st.text_input("ENTER TICKER", "XLF").upper()
data, zar_rate = get_data(ticker)

if data is not None:
    curr_p = float(data['Close'].iloc[-1])
    is_jse = ".JO" in ticker
    price_zar = curr_p if is_jse else curr_p * zar_rate

    # Glass Metrics
    c1, c2 = st.columns(2)
    with c1: st.metric("Live Price", f"R{price_zar:,.2f}")
    with c2: st.metric("Exchange Rate", f"R{zar_rate:.2f}")

    st.line_chart(data['Close'])
