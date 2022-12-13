import yfinance as yf
import datetime
from datetime import timedelta
from functools import lru_cache

INTERVALS = ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']

def get_ticker(stock):
    ticker = yf.Ticker(stock)
    return ticker


def validate_dt(date_text):
    if not date_text:
        return None
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        print("Incorrect data format, should be YYYY-MM-DD not ",date_text)
        return None
    return date_text


def get_6m_date_interval():
    delta = timedelta(days=180)
    today = datetime.datetime.now()
    return datetime.datetime.strftime(today - delta, '%Y-%m-%d'), \
           datetime.datetime.strftime(today, '%Y-%m-%d'),


@lru_cache(5)
def get_historical(stock, interval = '1d',st_dt=None, ed_dt=None):
    if not validate_dt(st_dt) or not validate_dt(ed_dt):
        st_dt, ed_dt = get_6m_date_interval()

    if interval not in INTERVALS:
        interval = '1d'

    tick = get_ticker(stock)

    historical = tick.history(start=st_dt, end=ed_dt, interval=interval)
    #['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits'],
    return historical


if __name__ == '__main__':
    df = get_historical('AAPL')
    df.to_csv('tmep.csv')