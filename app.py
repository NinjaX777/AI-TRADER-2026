import streamlit as st
import yfinance as yf
import pandas as pd

# --- 1. THE "MODERN GLASS" LOOK ---
st.set_page_config(page_title="My Simple Trader", layout="wide")

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%) !important;
    }
    [data-testid="stMetric"], .stTabs, div[data-baseweb="input"], .stSlider, .stInfo, .stSuccess {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(15px) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 20px !important;
        color: white !important;
    }
    h1, h2, h3, p, label { color: white !important; font-family: 'sans-serif'; }
</style>
""", unsafe_allow_html=True)

# --- 2. EASY LOGIN ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🛡️ Welcome to Your Trading App")
    st.write("Tap the button below to start.")
    if st.button("Unlock My Dashboard", use_container_width=True, type="primary"):
        st.session_state.authenticated = True
        st.rerun()
    st.stop()

# --- 3. THE "NO-GUESSING" SEARCH ---
st.title("📈 Simple Trading Center")

# We create a dictionary so you can pick by Name, not Ticker
search_options = {
    "Select a Company": "",
    "Absa Bank (SA)": "ABG.JO",
    "Sasol (SA)": "SOL.JO",
    "Naspers (SA)": "NPN.JO",
    "Standard Bank (SA)": "SBK.JO",
    "Apple (US)": "AAPL",
    "Tesla (US)": "TSLA",
    "Amazon (US)": "AMZN",
    "S&P 500 (US Top 500 Stocks)": "SPY"
}

selection = st.selectbox("Which company do you want to check?", list(search_options.keys()))
ticker = search_options[selection]

if ticker:
    with st.spinner('Loading market data...'):
        try:
            # Get the data
            data = yf.download(ticker, period="1y")
            if isinstance(data.columns, pd.MultiIndex):
                data.columns = data.columns.get_level_values(0)
            
            # Get Rand/Dollar exchange rate
            fx = yf.download("USDZAR=X", period="1d")['Close'].iloc[-1]
            
            price = float(data['Close'].iloc[-1])
            is_jse = ".JO" in ticker
            final_price_zar = price if is_jse else price * fx

            # --- DISPLAY SECTION ---
            st.subheader(f"Results for {selection}")
            
            c1, c2 = st.columns(2)
            c1.metric("Current Price (Rand)", f"R{final_price_zar:,.2f}")
            c2.metric("Rand/Dollar Rate", f"R{fx:.2f}")

            st.line_chart(data['Close'])

            # --- PLAIN ENGLISH ADVICE ---
            st.divider()
            st.subheader("💡 Simple Advice")
            
            ma200 = data['Close'].rolling(200).mean().iloc[-1]
            
            if price > ma200:
                st.success(f"✅ Looks good! {selection} is currently in a growing trend.")
                st.info(f"Strategy: If you have R10,000 to invest, buying R1,000 worth of this stock is a safe way to start.")
            else:
                st.warning(f"⚠️ Be careful. {selection} is currently losing value. It might be better to wait.")

        except Exception as e:
            st.error("Something went wrong. Please try selecting a different company.")

else:
    st.info("Please select a company from the list above to see its performance.")
