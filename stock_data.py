import yfinance as yf
import pandas as pd


def stock_symbols():
    df = pd.read_csv('stocks.csv')
    stocks = {'symbol': df['Symbol'], 'name': df['Name']}
    return stocks  # json.loads(r.content)


def get_data(stock):

    stck = stock.split(' ')[0]
    stock_data = yf.Ticker(stck)
    hist = stock_data.history(period="max")
    return hist
