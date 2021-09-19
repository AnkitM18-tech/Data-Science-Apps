#importing libraries
import yfinance as yf
import streamlit as stl
import pandas as pd

stl.write("""
    #Stock Price App

    Shown are the stock **Closing Price** and **Volume** of Google!

""")

#define ticker symbol
tickerSymbol = 'GOOGL'

# get data on this ticker
tickerData = yf.Ticker(tickerSymbol)

#get historical prices for this ticker
tickerDf = tickerData.history(period='1d',start='2011-9-19',end='2021-9-19')

#Open High Low Close Volume Dividends Stock Splits -- options

stl.line_chart(tickerDf.Close)
stl.line_chart(tickerDf.Volume)