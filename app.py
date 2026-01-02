from streamlit_gsheets import GSheetsConnection
import streamlit as st
import yfinance as yf
import pandas as pd

# --- SECURITY ---
ACCESS_PASSWORD = "YourSecretKey2026" 

def check_password():
    if "authenticated" not in st.session_state:
        st.title("🔐 AI Trader Secure Login")
        pwd = st.text_input("Enter Access Key", type="password")
        if st.button("Access Dashboard"):
            if pwd == ACCESS_PASSWORD:
                st.session_state.authenticated = True
                st.rerun()
            else: st.error("Invalid Key")
        return False
    return True

if not check_password(): st.stop()

# --- APP CONFIG ---
st.set_page_config(page_title="2026 Elite Trader", layout="wide")

# --- SIDEBAR: GOALS & GUIDES ---
with st.sidebar:
    st.header("🎯 2026 Trading Goals")
    st.info("""
    - **Primary Goal:** 15-20% Annual Growth.
    - **Risk Limit:** Never lose >1% per trade.
    - **Focus:** Institutional Sector Rotation.
    """)
    
    st.header("📖 Instructions")
    with st.expander("How to Trade"):
        st.write("""
        1. **Pick Ticker:** Enter US or JSE symbols.
        2. **Check Signal:** Only buy if Green.
        3. **Risk Calc:** Enter your Rand balance.
        4. **Execute:** Place order with your broker.
        """)

# --- MAIN ENGINE ---
st.title("📈 AI Trader Command Center (ZAR Optimized)")

# Currency Conversion Logic
try:
    usd_zar = yf.download("USDZAR=X", period="1d")['Close'].iloc[-1]
except:
    usd_zar = 18.50 # Fallback

ticker = st.text_input("Enter Ticker (US: XLF | JSE: ABG.JO)", "XLF").upper()

@st.cache_data(ttl=3600)
def get_data(symbol):
    df = yf.download(symbol, period="1y")
    if df.empty: return None
    df['MA200'] = df['Close'].rolling(200).mean()
    # RSI Calculation
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    df['RSI'] = 100 - (100 / (1 + (gain/loss)))
    return df

data = get_data(ticker)

if data is not None:
    curr_p = float(data['Close'].iloc[-1])
    ma200 = float(data['MA200'].iloc[-1])
    rsi = float(data['RSI'].iloc[-1])
    is_jse = ticker.endswith(".JO")

    # Layout
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader(f"Analysis: {ticker}")
        st.line_chart(data['Close'])
        
        if curr_p > ma200 and rsi < 70:
            st.success("✅ BUY SIGNAL: Trend is up. High Probability.")
        elif rsi > 70:
            st.warning("⚠️ OVERBOUGHT: Price is too high. Wait for dip.")
        else:
            st.error("❌ AVOID: Downtrend detected.")

    with col2:
        st.subheader("🛡️ Risk Manager (ZAR)")
        balance_zar = st.number_input("Account Balance (R)", value=100000)
        risk_pct = st.slider("Risk (%)", 0.5, 2.0, 1.0)
        
        # Convert Price for US stocks to ZAR
        display_price = curr_p if is_jse else curr_p * usd_zar
        st.metric("Price (ZAR Equivalent)", f"R{display_price:,.2f}")
        
        stop_loss_zar = st.number_input("Stop Loss (R)", value=display_price * 0.95)
        
        risk_amt_zar = balance_zar * (risk_pct / 100)
        risk_per_share = display_price - stop_loss_zar
        
        if risk_per_share > 0:
            shares = int(risk_amt_zar / risk_per_share)
            st.info(f"ACTION: Buy {shares} shares")
            st.write(f"Risking R{risk_amt_zar:,.2f} on this trade.")
        else:
            st.warning("Set Stop Loss below price.")

st.divider()
st.caption(f"Live USD/ZAR Rate: R{usd_zar:.2f} | Data updated for January 2026")
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    df['RSI'] = 100 - (100 / (1 + (gain/loss)))
    return df

data = get_data(ticker)

if data is not None:
    curr_p = float(data['Close'].iloc[-1])
    ma200 = float(data['MA200'].iloc[-1])
    rsi = float(data['RSI'].iloc[-1])

    tab1, tab2 = st.tabs(["📊 Market Signal", "🛡️ Risk Manager"])

    with tab1:
        st.metric(ticker, f"R{curr_p:.2f}")
        st.line_chart(data['Close'])
        
        if curr_p > ma200 and rsi < 70:
            st.success("✅ BUY SIGNAL: Trend is up and not overbought.")
        elif rsi > 70:
            st.warning("⚠️ OVERBOUGHT: Price is high. Wait for pullback.")
        else:
            st.error("❌ AVOID: Asset is in a downtrend (Below 200MA).")

    with tab2:
        balance = st.number_input("Account Balance (R)", value=10000)
        risk_pct = st.slider("Risk Per Trade (%)", 0.5, 2.0, 1.0)
        stop_loss = st.number_input("Stop Loss Price (R)", value=curr_p * 0.95)
        
        risk_amt = balance * (risk_pct / 100)
        shares = int(risk_amt / (curr_p - stop_loss)) if curr_p > stop_loss else 0
        
        st.info(f"ACTION: Buy {shares} shares")
        st.write(f"This risks exactly R{risk_amt:.2f} of your capital.")

