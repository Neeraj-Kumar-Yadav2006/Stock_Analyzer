import streamlit as st
import requests
import yfinance as yf

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="AI Financial Intelligence Agent",
    page_icon="📊",
    layout="wide"
)

# ---------------- TITLE ---------------- #

st.title("📊 AI Financial Intelligence Agent Platform")
st.markdown(
    "AI-powered stock analysis, sentiment insights, and market intelligence"
)

st.divider()

# ---------------- SIDEBAR ---------------- #

st.sidebar.header("📈 Stock Analyzer")

popular_stocks = [
    "AAPL",
    "TSLA",
    "MSFT",
    "GOOGL",
    "AMZN",
    "NVDA",
    "META",
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS"
]

ticker = st.sidebar.selectbox("Choose Stock", popular_stocks)

analyze = st.sidebar.button("Analyze Stock")

# ---------------- LAYOUT ---------------- #

col1, col2 = st.columns(2)

# ---------------- ANALYSIS ---------------- #

if analyze:

    url = f"http://127.0.0.1:8000/analyze/{ticker}"

    with st.spinner("Analyzing stock using AI..."):

        try:
            response = requests.get(url)

            if response.status_code == 200:

                data = response.json()

                # -------- AI SUMMARY -------- #

                st.subheader("🤖 AI Financial Summary")

                summary = data.get("summary", "No summary available")

                st.success(summary)

                st.divider()

                # -------- STOCK CHART -------- #

                st.subheader("📈 Stock Price Chart (Last 6 Months)")

                stock = yf.Ticker(ticker)

                hist = stock.history(period="6mo")

                if not hist.empty:
                    st.line_chart(hist["Close"])
                else:
                    st.warning("No stock data available")

                st.divider()

                # -------- METRICS + SENTIMENT -------- #

                with col1:

                    st.subheader("📊 Stock Metrics")

                    metrics = data.get("stock_metrics", {})

                    st.json(metrics)

                with col2:

                    st.subheader("📰 News Sentiment")

                    sentiment = data.get("sentiment", {})

                    st.json(sentiment)

            else:
                st.error(f"Backend Error: {response.status_code}")

        except Exception as e:

            st.error(f"Connection Error: {e}")