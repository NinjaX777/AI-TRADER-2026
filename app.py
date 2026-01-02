import streamlit as st
import yfinance as yf
import pandas as pd

# 1. ULTIMATE MOBILE CSS OVERRIDE (FORCED GLASS)
st.set_page_config(page_title="ZAR Elite Trader", layout="wide")

st.markdown("""
<style>
    /* Force deep gradient background */
    .stApp {
        background: linear-gradient(160deg, #020024 0%, #090979 35%, #00d4ff 100%) !important;
        background-attachment: fixed !important;
    }

    /* Brute-force transparency on ALL streamlit layers */
    .st-emotion-cache-1835u1r, .st-emotion-cache-z5fcl4, .st-emotion-cache-6qob1r {
        background-color: transparent !important;
    }

    /* The Glass Hack: Uses fixed positioning and backdrop-filter to survive Mobile Chrome */
    [data-testid="stMetric"], .stSelectbox, div[data-baseweb="input"], .stAlert {
        background: rgba(255, 255, 255, 0.07) !important;
        backdrop-filter: blur(25px) saturate(200%) !important;
        -webkit-backdrop-filter: blur(25px) saturate(200%) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 25px !important;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.6) !important;
        margin-bottom: 20px !important;
    }

    /* Razor-sharp text for small screens */
    h1, h2, h3, p, label, .stMetric label {
        color: #ffffff !important;
        font-family: 'Inter', sans-serif !important;
        text-shadow: 0px 3px 6px rgba(0,0,0,0.9) !important;
    }
</style>
""", unsafe_allow_html=True)

# 2. THE COMMAND CENTER (SMART SELECTION)
st.title("🛡️ Command Center")

# Beginner-friendly Search Dictionary
options = {
    "Select a Company": "",
    "Absa Bank": "ABG.JO",
    "Sasol (Energy)": "SOL.JO",
    "Naspers (Tech)": "NPN.JO",
    "FirstRand (FNB)": "FSR.JO",
    "Standard Bank": "SBK.JO",
    "Capitec Bank": "CPI.JO",
    "Apple (iPhone)": "AAPL",
    "Tesla (Elon Musk)": "TSLA"
}

selection = st.selectbox("Search Company Name:", list(options.keys()))
ticker = options[selection]

if ticker:
    try:
        # DATA SHIELD: Prevents the MultiIndex crash
        df = yf.download(ticker, period="1y", interval="1d", auto_adjust=True)
        
        if not df.empty:
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

            # Live USD/ZAR conversion
            fx_data = yf.download("USDZAR=X", period="1d")
            fx = fx_data['Close'].iloc[-1] if not fx_df.empty else 18.20
            
            price = float(df['Close'].iloc[-1])
            is_jse = ".JO" in ticker
            price_zar = price if is_jse else price * fx
            
            # VISUALS
            m1, m2 = st.columns(2)
            m1.metric("Live Price (Rand)", f"R{price_zar:,.2f}")
            m2.metric("USD/ZAR Rate", f"R{fx:.2f}")

            st.area_chart(df['Close'])

            # PLAIN ENGLISH GUIDANCE
            st.divider()
            avg = df['Close'].rolling(200).mean().iloc[-1]
            if price > avg:
                st.success(f"🟢 {selection} is Trending UP (Strong).")
            else:
                st.warning(f"🔴 {selection} is Trending DOWN (Wait).")
        else:
            st.error("Market data currently unavailable. Try another.")

    except Exception as e:
        st.error("Connection error. Refresh your browser.")
else:
    st.info("Tap the box above to pick a company and start.")
