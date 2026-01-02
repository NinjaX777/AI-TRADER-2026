from streamlit_gsheets import GSheetsConnection
import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

# --- SECURITY ---
ACCESS_PASSWORD = "P@$sw0R_d1992" # CHANGE THIS

def check_password():
    if "authenticated" not in st.session_state:
        st.title("🔐 Secure Access")
        pwd = st.text_input("Enter Access Key", type="password")
        if st.button("Login"):
            if pwd == ACCESS_PASSWORD:
                st.session_state.authenticated = True
                st.rerun()
            else: st.error("Invalid Key")
        return False
    return True

if not check_password(): st.stop()

# --- APP LOGIC ---
st.set_page_config(page_title="2026 AI Trader", layout="centered")
st.title("📈 AI Trader Command Center")

ticker = st.text_input("Enter Ticker (e.g., XLF, INDA, VIG)", "XLF").upper()

@st.cache_data(ttl=3600)
def get_data(symbol):
    df = yf.download(symbol, period="1y")
    if df.empty: return None
    df['MA200'] = df['Close'].rolling(200).mean()
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

