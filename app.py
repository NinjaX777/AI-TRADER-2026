import streamlit as st
import yfinance as yf
import pandas as pd

# 1. THE GLASS UI ENGINE (REWRITTEN FOR 2026 STABILITY)
st.set_page_config(page_title="AI Trader ZAR", layout="wide")

st.markdown("""
<style>
    /* Gradient Background so you can actually see the glass effect */
    .stApp {
        background: linear-gradient(145deg, #0e1117 0%, #1c1f2b 100%) !important;
    }

    /* Glass Panels: These target the actual metric and input wrappers */
    [data-testid="stMetric"], [data-testid="stMetricValue"], .stTabs, div[data-baseweb="input"] {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px !important;
        padding: 15px !important;
    }

    /* Ensure text is always white and readable */
    h1, h2, h3, p, label {
        color: white !important;
        font-family: 'sans-serif';
    }
</style>
""", unsafe_allow_html=True)

# 2. SIMPLE SECURITY (NO TRICKS)
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🛡️ Secure Access")
    if st.button("Unlock Dashboard", use_container_width=True):
        st.session_state.authenticated = True
        st.rerun()
    st.stop()

# 3. CORE TRADING TOOLS
st.title("📈 AI Command Center")

@st.cache_data(ttl=3600)
def get_market_data(ticker):
    try:
        df = yf.download(ticker, period="1y")
        # Fix for 2026 yfinance MultiIndex data
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
            
        fx_df = yf.download("USDZAR=X", period="1d")
        fx = fx_df['Close'].iloc[-1] if not fx_df.empty else 18.50
        return df, float(fx)
    except:
        return None, 18.50

symbol = st.text_input("ENTER TICKER (e.g. XLF or ABG.JO)", "XLF").upper()
data, zar_rate = get_market_data(symbol)

if data is not None and not data.empty:
    price = float(data['Close'].iloc[-1])
    is_jse = ".JO" in symbol
    price_zar = price if is_jse else price * zar_rate

    # The Visual Layout
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Live Price (ZAR)", f"R{price_zar:,.2f}")
    with col2:
        st.metric("ZAR Rate", f"R{zar_rate:.2f}")

    st.line_chart(data['Close'])
    
    st.subheader("🛡️ Risk & Goals")
    st.info("Goal: 20% Growth | Risk: 1% per trade")
    
    balance = st.number_input("Account Balance (R)", value=100000)
    stop_loss = st.number_input("Stop Loss (R)", value=price_zar * 0.95)
    
    risk_rands = balance * 0.01
    loss_per_share = price_zar - stop_loss
    
    if loss_per_share > 0:
        shares = int(risk_rands / loss_per_share)
        st.success(f"👉 ACTION: Buy {shares} shares of {symbol}")
    
else:
    st.error("Waiting for valid ticker input...")
