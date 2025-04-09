
import streamlit as st
import pandas as pd

def analyze_market_and_recommend_stocks(investment_amount):
    stock_data = [
        {
            "Stock Name": "Tata Motors",
            "Sector": "Automobile",
            "Signal": "Buy",
            "Entry Price (₹)": 900,
            "Stop Loss (₹)": 860,
            "Target Price (₹)": 1020,
            "Expected Return (%)": 13.33
        },
        {
            "Stock Name": "Infosys",
            "Sector": "IT Services",
            "Signal": "Buy",
            "Entry Price (₹)": 1420,
            "Stop Loss (₹)": 1360,
            "Target Price (₹)": 1600,
            "Expected Return (%)": 12.68
        },
        {
            "Stock Name": "HDFC Bank",
            "Sector": "Banking",
            "Signal": "Sell",
            "Entry Price (₹)": 1450,
            "Stop Loss (₹)": 1480,
            "Target Price (₹)": 1370,
            "Expected Return (%)": -5.52
        }
    ]
    
    df = pd.DataFrame(stock_data)
    df["Capital Allocation (₹)"] = investment_amount / len(df)
    df["Potential Profit (₹)"] = (df["Capital Allocation (₹)"] * df["Expected Return (%)"]) / 100
    return df

# Streamlit UI
st.set_page_config(page_title="ProfitPulse AI", layout="wide")
st.title("ProfitPulse AI: Real-Time Stock Recommendation Engine")

investment_amount = st.number_input("Enter the amount you want to invest (₹):", min_value=1000, step=1000)

if investment_amount:
    result_df = analyze_market_and_recommend_stocks(investment_amount)
    st.subheader("Recommended Stock Actions")
    st.dataframe(result_df, use_container_width=True)
