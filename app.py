import streamlit as st
import yfinance as yf
import pandas as pd

# --- 1. GLASSMORPHISM UI THEME ---
st.set_page_config(page_title="AI Trader Elite", layout="wide")

glass_style = """
<style>
    /* Background Image */
    .stApp {
        background: linear-gradient(135deg, #1e1e2f 0%, #0d0d15 100%);
    }

    /* Glass Effect Containers */
    div[data-testid="stVerticalBlock"] > div:has(div.stMetric), 
    .stTabs, .stExpander, .stTextInput, .stNumberInput, .stSlider {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }

    /* Sidebar Glass Effect */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 15, 25, 0.7) !important;
        backdrop-filter: blur(10px);
    }

    /* Customizing Text Colors for Readability */
    h1, h2, h3, p, .stMetric label {
        color: #ffffff !important;
        font-family: 'Inter', sans-serif;
    }
</style>
"""
st.markdown(glass_style, unsafe_allow_html=True)

# --- 2. SECURITY & SESSION ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def login_callback():
    st.session_state.authenticated = True

if not st.session_state.authenticated:
    st.title("🧬 Biometric Gateway")
    st.markdown("### Please authenticate to access the 2026 Trading Floor.")
    st.button("🧬 Verify Identity", on_click=login_callback, use_container_width=True, type="primary")
    st.stop()

# --- 3. DASHBOARD LOGIC ---
st.title("🛡️ AI Command Center")

# Sidebar for Goals & Instructions
with st.sidebar:
    st.title("🎯 Strategy Panel")
    st.markdown("---")
    st.markdown("#### **2026 Goals**")
    st.success("Target: 20% Alpha\nRisk: 1% Max per Trade")
    st.markdown("---")
    if st.button("Secure Logout"):
        st.session_state.authenticated = False
        st.rerun()

# Data Engine
@st.cache_data(ttl=3600)
def get_advanced_data(symbol):
    try:
        df = yf.download(symbol, period="1y")
        fx = yf.download("USDZAR=X", period="1d")['Close'].iloc[-1]
        df['MA200'] = df['Close'].rolling(200).mean()
        # RSI
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        df['RSI'] = 100 - (100 / (1 + (gain/loss)))
        return df, fx
    except: return None, 18.50

ticker = st.text_input("ENTER TICKER", "XLF").upper()
data, zar_rate = get_advanced_data(ticker)

if data is not None:
    curr_p = float(data['Close'].iloc[-1])
    ma200 = float(data['MA200'].iloc[-1])
    rsi = float(data['RSI'].iloc[-1])
    is_jse = ticker.endswith(".JO")
    price_zar = curr_p if is_jse else curr_p * zar_rate

    # Glassmorphic Metrics
    m1, m2, m3 = st.columns(3)
    m1.metric("Live Price (ZAR)", f"R{price_zar:,.2f}")
    m2.metric("Trend (200MA)", f"{ma200:.2f}")
    m3.metric("Momentum (RSI)", f"{rsi:.1f}")

    tab1, tab2 = st.tabs(["📈 Market Visuals", "🛡️ Position Management"])

    with tab1:
        st.line_chart(data['Close'])
        if curr_p > ma200 and rsi < 70:
            st.success("✅ BULLISH SIGNAL: Enter Trade")
        else:
            st.error("❌ CAUTION: Trend Weak or Overbought")

    with tab2:
        st.markdown("#### **Risk Calculator**")
        balance = st.number_input("Account Balance (R)", value=100000)
        risk_pct = st.slider("Risk Tolerance %", 0.5, 2.0, 1.0)
        stop_loss = st.number_input("Stop Loss (R)", value=price_zar * 0.95)
        
        risk_rands = balance * (risk_pct / 100)
        loss_per_share = price_zar - stop_loss
        
        if loss_per_share > 0:
            shares = int(risk_rands / loss_per_share)
            st.info(f"👉 **EXECUTION:** Buy **{shares}** shares")
            st.write(f"ZAR Risk: R{risk_rands:,.2f}")

st.divider()
st.caption(f"System: Advanced Trader Agent | USDZAR: R{zar_rate:.2f}")
