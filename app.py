import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Options Volatility App", layout="wide")

st.title("📈 Options Volatility Analysis")

# User input
ticker = st.text_input("Enter a stock ticker symbol:", "AAPL")

# Fetch historical price data
try:
    data = yf.download(ticker, period="6mo", interval="1d")
    if data.empty:
        st.error("No data found. Please check the ticker symbol.")
    else:
        # Calculate daily log returns
        data['Log Return'] = np.log(data['Close'] / data['Close'].shift(1))
        data.dropna(inplace=True)
        
        # Calculate Historical Volatility (HV)
        hv = data['Log Return'].std() * np.sqrt(252) * 100  # Annualized in %
        st.write(f"**Historical Volatility (HV): {hv:.2f}%**")
        
        # (Simplified) Implied Volatility Proxy (IV)
        # Note: yfinance doesn't directly provide IV — you’d need options chain data for real IV.
        # Here we use the 30-day rolling standard deviation as a naive proxy.
        data['HV_30'] = data['Log Return'].rolling(window=30).std() * np.sqrt(252) * 100
        
        # Plot Historical Volatility
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(data.index, data['HV_30'], label="30-day HV Proxy")
        ax.set_title(f"{ticker} - 30-day Historical Volatility")
        ax.set_xlabel("Date")
        ax.set_ylabel("Volatility (%)")
        ax.legend()
        st.pyplot(fig)

        # Display raw data table
        if st.checkbox("Show raw data"):
            st.dataframe(data[['Close', 'HV_30']].dropna())
except Exception as e:
    st.error(f"Error fetching data: {e}")
