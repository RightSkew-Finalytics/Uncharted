import pandas_ta as ta
import yfinance as yf
import datetime as dt
import pandas as pd




def calculate_macd(symbol):
    # Request historic pricing data via finance.yahoo.com API
    df = yf.Ticker(symbol).history(period='1y')[['Close', 'Open', 'High', 'Volume', 'Low']]
    # Calculate MACD values using the pandas_ta library
    df.ta.macd(close='close', fast=12, slow=26, signal=9, append=True)
    print("Macd Line : ",round(df['MACD_12_26_9'].iloc[-1],2))
    print("Macd Signal : ",round(df['MACDs_12_26_9'].iloc[-1],2))


calculate_macd("AARON.NS")
