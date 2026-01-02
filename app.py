import streamlit as st
import pandas as pd
import numpy as np
try:
    import plotly.graph_objects as go
except ImportError:
    st.error("Missing library: plotly. Please check your requirements.txt file.")
from alpha_vantage.timeseries import TimeSeries
from sklearn.linear_model import LinearRegression
from datetime import timedelta

# --- 1. CONFIG & SECRETS ---
try:
    API_KEY = st.secrets["AV_KEY"]
except:
    API_KEY = "MISSING"

st.set_page_config(page_title="AI TRADER ELITE v2026", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    [data-testid="stMetricValue"] { color: #00FF41; font-family: 'monospace'; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA ENGINE ---
def get_clean_data(symbol):
    try:
        ts = TimeSeries(key=API_KEY, output_format='pandas')
        data, _ = ts.get_daily(symbol=symbol, outputsize='compact')
        data.columns = [c.split('. ')[1].capitalize() for c in data.columns]
        data.index = pd.to_datetime(data.index)
        return data.sort_index()
    except Exception as e:
        st.error(f"API Error: {e}")
        return pd.DataFrame()

# --- 3. AI FORECAST ENGINE ---
def run_ai_logic(df):
    X = np.arange(len(df)).reshape(-1, 1)
    y = df['Close'].values
    model = LinearRegression().fit(X, y)
    future_indices = np.arange(len(df), len(df) + 7).reshape(-1, 1)
    predictions = model.predict(future_indices)
    last_date = df.index[-1]
    future_dates = [(last_date + timedelta(days=i)).date() for i in range(1, 8)]
    forecast_df = pd.DataFrame({'Date': future_dates, 'Prediction': predictions})
    return forecast_df, model.coef_[0]

# --- 4. MAIN INTERFACE ---
st.title("📟 AI TRADER ELITE")
ticker = st.text_input("SYMBOL", value="AAPL").upper()

if API_KEY == "MISSING":
    st.warning("Paste your key in Streamlit Secrets as AV_KEY")
elif ticker:
    df = get_clean_data(ticker)
    if not df.empty:
        forecast_df, trend_slope = run_ai_logic(df)
        last_price = df['Close'].iloc[-1]
        
        c1, c2, c3 = st.columns(3)
        c1.metric("CURRENT", f"${last_price:,.2f}")
        c2.metric("TARGET", f"${forecast_df['Prediction'].iloc[0]:,.2f}")
        c3.metric("BIAS", "BULLISH" if trend_slope > 0 else "BEARISH")

        fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
        fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("🗓️ 7-DAY FORECAST")
        st.table(forecast_df.set_index('Date'))
