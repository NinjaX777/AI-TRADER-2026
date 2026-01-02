import streamlit as st
import pandas as pd
import numpy as np
from alpha_vantage.timeseries import TimeSeries
from sklearn.linear_model import LinearRegression

# --- 1. DATA SECRETS ---
# This looks for the key you will paste into the Streamlit Cloud Settings
try:
    API_KEY = st.secrets["AV_KEY"]
except:
    API_KEY = "MISSING"

st.set_page_config(page_title="AI TRADER ELITE v2026", layout="wide")

# Matrix-style UI
st.markdown("<style>.stApp { background-color: #050505; color: #00FF41; } [data-testid='stMetricValue'] { color: #00FF41; font-family: 'Courier New'; }</style>", unsafe_allow_html=True)

# --- 2. DATA ENGINE ---
def get_clean_data(symbol):
    try:
        ts = TimeSeries(key=API_KEY, output_format='pandas')
        data, _ = ts.get_daily(symbol=symbol, outputsize='compact')
        data.columns = [c.split('. ')[1].capitalize() for c in data.columns]
        data.index = pd.to_datetime(data.index)
        return data.sort_index()
    except Exception as e:
        st.error(f"API Connection Error: {e}")
        return pd.DataFrame()

# --- 3. AI ENGINE ---
def run_ai_prediction(df):
    df = df.reset_index()
    df['Day_Count'] = np.arange(len(df))
    X = df[['Day_Count']].values
    y = df['Close'].values
    model = LinearRegression().fit(X, y)
    prediction = model.predict([[len(df)]])[0]
    return prediction, model.coef_[0]

# --- 4. INTERFACE ---
st.title("📟 AI TRADER ELITE")
ticker = st.sidebar.text_input("SYMBOL", value="AAPL").upper()

if API_KEY == "MISSING":
    st.warning("⚠️ Go to Streamlit Settings > Secrets and add: AV_KEY = 'your_key'")
else:
    df = get_clean_data(ticker)
    if not df.empty:
        pred, trend = run_ai_prediction(df)
        last = df['Close'].iloc[-1]
        c1, c2, c3 = st.columns(3)
        c1.metric("CURRENT", f"${last:,.2f}")
        c2.metric("AI PREDICTION", f"${pred:,.2f}", delta=f"{pred-last:.2f}")
        c3.metric("TREND", "BULLISH" if trend > 0 else "BEARISH")
        st.line_chart(df['Close'])
