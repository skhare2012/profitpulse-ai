import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
from ta.momentum import RSIIndicator
from ta.trend import MACD
from textblob import TextBlob

# Replace with your own API key
ALPHA_VANTAGE_API_KEY = "YOUR_ALPHA_VANTAGE_API_KEY"
NEWS_API_KEY = "YOUR_NEWS_API_KEY"

st.set_page_config(page_title="ProfitPulse AI", layout="wide")
st.title("📈 ProfitPulse AI: Real-Time Stock Recommendation Engine")

investment_amount = st.number_input("💰 Enter amount to invest (₹):", min_value=1000, step=1000)
risk_profile = st.selectbox("🧠 Select your risk profile:", ["Low", "Moderate", "High"])
sector_filter = st.text_input("🏭 Filter by Sector (optional):")

# Placeholder for stock list (could be fetched from NSE API or CSV)
stocks_to_analyze = ["TCS.BSE", "INFY.BSE", "RELIANCE.BSE", "HDFCBANK.BSE", "TATAMOTORS.BSE"]

@st.cache_data

def get_stock_data(symbol):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}&outputsize=compact"
    r = requests.get(url)
    data = r.json()
    prices = data.get("Time Series (Daily)", {})
    df = pd.DataFrame(prices).T
    df = df.rename(columns={
        "1. open": "Open", "2. high": "High", "3. low": "Low", "4. close": "Close", "5. volume": "Volume"
    })
    df = df.astype(float)
    df.index = pd.to_datetime(df.index)
    return df.sort_index()

@st.cache_data

def get_sentiment(stock_name):
    url = f"https://newsapi.org/v2/everything?q={stock_name}&apiKey={NEWS_API_KEY}"
    response = requests.get(url).json()
    articles = response.get("articles", [])
    sentiment_score = 0
    for article in articles[:5]:
        blob = TextBlob(article.get("title", ""))
        sentiment_score += blob.sentiment.polarity
    return sentiment_score / max(len(articles), 1)

def generate_recommendations():
    recommendations = []
    for stock in stocks_to_analyze:
        try:
            df = get_stock_data(stock)
            latest_close = df["Close"].iloc[-1]
            rsi = RSIIndicator(df["Close"]).rsi().iloc[-1]
            macd = MACD(df["Close"]).macd_diff().iloc[-1]
            sentiment = get_sentiment(stock.split(".")[0])

            signal = "Hold"
            if rsi < 30 and macd > 0 and sentiment > 0:
                signal = "Buy"
            elif rsi > 70 and macd < 0 and sentiment < 0:
                signal = "Sell"

            recommendations.append({
                "Stock": stock,
                "Price (₹)": latest_close,
                "RSI": round(rsi, 2),
                "MACD": round(macd, 2),
                "Sentiment": round(sentiment, 2),
                "Signal": signal
            })
        except Exception as e:
            st.warning(f"⚠️ Failed to fetch for {stock}: {e}")

    df_rec = pd.DataFrame(recommendations)
    df_rec = df_rec.sort_values(by=["Signal", "Sentiment"], ascending=[False, False])
    df_rec["Allocation (₹)"] = investment_amount / len(df_rec)
    df_rec["Potential Gain (₹)"] = df_rec["Allocation (₹)"] * 0.10  # Hypothetical 10% return
    return df_rec

if st.button("🔍 Analyze & Recommend"):
    result_df = generate_recommendations()
    st.subheader("📊 Stock Recommendations")
    st.dataframe(result_df, use_container_width=True)

    buy_stocks = result_df[result_df["Signal"] == "Buy"]
    if not buy_stocks.empty:
        st.success("✅ Suggested Buys")
        st.table(buy_stocks[["Stock", "Price (₹)", "RSI", "Sentiment", "Potential Gain (₹)"]])
    else:
        st.info("No strong buy signals right now. Check back later!")
