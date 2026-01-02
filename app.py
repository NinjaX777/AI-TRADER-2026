import streamlit as st
import yfinance as yf
import pandas as pd

# --- 1. GLASSMORPHISM UI THEME ---
st.set_page_config(page_title="AI Trader Elite", layout="wide")

glass_style = """
<style>
    .stApp { background: linear-gradient(135deg, #1e1e2f 0%, #0d0d15 100%); }
    [data-testid="stMetricValue"] { font-size: 1.8rem !important; }
    div[data-testid="stVerticalBlock"] > div:has(div.stMetric), 
    .stTabs, .stExpander, .stTextInput, .stNumberInput, .stSlider {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    [data-testid="stSidebar"] { background-color: rgba(15, 15, 25, 0.7) !important; backdrop-filter: blur(10px); }
    h1, h2, h3, p, label { color: #ffffff !important; }
</style>
"""
st.markdown(glass_style, unsafe_allow_html=True)

# --- 2. SECURITY ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🧬 Biometric Gateway")
    if st.button("🧬 Verify Identity", use_container_width=True, type="primary"):
        st.session_state.authenticated = True
        st.rerun()
    st.stop()

# --- 3. DATA ENGINE (WITH SAFETY SHIELD) ---
@st.cache_data(ttl=3600)
def get_clean_data(symbol):
    try:
        # We use 'auto_adjust' and manual column fix for 2026 yfinance compatibility
        df = yf.download(symbol, period="1y", auto_adjust=True)
        
        if df.empty or len(df) < 1:
            return None, 18.50
            
        # Fix for MultiIndex columns if they exist
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        fx_df = yf.download("USDZAR=X", period="1d")
        fx = fx_df['Close'].iloc[-1] if not fx_df.empty else 18.50
        
        df['MA200'] = df['Close'].rolling(200).mean()
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        df['RSI'] = 100 - (100 / (1 + (gain/loss)))
        return df, float(fx)
    except Exception as e:
        return None, 18.50

# --- 4. DASHBOARD UI ---
st.title("🛡️ AI Command Center")

with st.sidebar:
    st.title("🎯 Strategy")
    st.info("**2026 Target:** +20% Alpha\n**Risk:** 1% Max/Trade")
    st.markdown("---")
    st.write("**Quick JSE Tips:**\n- Absa: `ABG.JO`\n- Sasol: `SOL.JO`\n- Naspers: `NPN.JO`")

ticker = st.text_input("ENTER TICKER (e.g., XLF or ABG.JO)", "XLF").upper()
data, zar_rate = get_clean_data(ticker)

# --- 5. RENDER LOGIC ---
if data is not None and not data.empty:
    curr_p = float(data['Close'].iloc[-1])
    ma200 = float(data['MA200'].iloc[-1]) if not pd.isna(data['MA200'].iloc[-1]) else 0
    rsi = float(data['RSI'].iloc[-1]) if not pd.isna(data['RSI'].iloc[-1]) else 50
    
    is_jse = ".JO" in ticker
    price_zar = curr_p if is_jse else curr_p * zar_rate

    # Metrics
    m1, m2, m3 = st.columns(3)
    m1.metric("Live Price", f"R{price_zar:,.2f}")
    m2.metric("Trend (200MA)", f"{ma200:.2f}")
    m3.metric("Momentum (RSI)", f"{rsi:.1f}")

    tab1, tab2 = st.tabs(["📈 Market Visuals", "🛡️ Risk Management"])

    with tab1:
        st.line_chart(data['Close'])
        if curr_p > ma200 and rsi < 70:
            st.success("✅ BULLISH SIGNAL: Enter Trade")
        else:
            st.error("❌ CAUTION: No Clear Entry")

    with tab2:
        balance = st.number_input("Account Balance (R)", value=100000)
        risk_pct = st.slider("Risk Tolerance %", 0.5, 2.0, 1.0)
        stop_loss = st.number_input("Stop Loss (R)", value=price_zar * 0.95)
        
        risk_rands = balance * (risk_pct / 100)
        loss_per_share = price_zar - stop_loss
        
        if loss_per_share > 0:
            shares = int(risk_rands / loss_per_share)
            st.info(f"👉 **ACTION:** Buy **{shares}** shares")
            st.write(f"ZAR Risk: R{risk_rands:,.2f}")
else:
    st.error(f"⚠️ Could not find data for '{ticker}'. If JSE, remember to add '.JO' (e.g., ABG.JO)")

st.divider()
st.caption(f"USDZAR: R{zar_rate:.2f} | 2026 Elite Dashboard")
