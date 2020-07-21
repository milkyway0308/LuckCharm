import requests
from bs4 import BeautifulSoup
from Alpha_Vantage.alpha_vantage.alphavantage import AlphaVantage
from Alpha_Vantage.alpha_vantage.timeseries import TimeSeries
import pandas
from LuckCharm.Data.APIKey import keys
import yfinance as yf

def collect(limit):
    a = AlphaVantage("")


if __name__ == '__main__':
    ser = TimeSeries(keys().alphaVantage(), output_format="pandas", indexing_type='date')
    panda = ser.get_daily(symbol='012790', outputsize='full')
    print(panda)
