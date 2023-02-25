#!pip install yfinance
# !pip install mplfinance
import pandas as pd
import yfinance as yf
from datetime import datetime, time


def loadData(ticker='BTC-USD', start_date=datetime(2015, 1, 1), end_date=datetime.now()):
    data = yf.download(ticker, start=start_date, end=end_date)
    data.to_csv("data/" + ticker + ".csv")


def csv_data(ticker):
    try:
        data = pd.read_csv("data/" + ticker + ".csv", index_col=0, parse_dates=True, infer_datetime_format=True)
        if data.iloc[-1].name == datetime.combine(datetime.now(), time.min):
            return data
        else:
            return loadAndGet(ticker)
    except:
        return loadAndGet(ticker)


def loadAndGet(ticker):
    loadData(ticker)
    return pd.read_csv("data/" + ticker + ".csv", index_col=0, parse_dates=True, infer_datetime_format=True)


BTC = csv_data("BTC-USD")
SOL = csv_data("SOL-USD")
DOT = csv_data("DOT-USD")
ETH = csv_data("ETH-USD")
XMR = csv_data("XMR-USD")
ATOM = csv_data("ATOM-USD")
AR = csv_data("AR-USD")
ADA = csv_data("ADA-USD")

GOOG = csv_data("GOOG")
MSFT = csv_data("MSFT")
ADBE = csv_data("ADBE")
NVDA = csv_data("NVDA")
ZM = csv_data("ZM")

if __name__ == '__main__':
    print(GOOG.tail())
    print(BTC.tail())
    print(SOL.tail())
    print(DOT.tail())
    print(ETH.tail())
    print(XMR.tail())
    print(ATOM.tail())
    print(AR.tail())
    print(ADA.tail())
