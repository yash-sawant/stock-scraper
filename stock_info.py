import pandas as pd
import yfinance as yf
import datetime
from datetime import timedelta
from functools import lru_cache
import traceback
from prediction import dt_func

INTERVALS = ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']

STACK_CACHE_PATH = 'stock_cache.csv'
df_cache = pd.read_csv(STACK_CACHE_PATH)
df_cache['Date'] = df_cache.Date.apply(lambda dt: dt[:10])
COLUMNS = ['Open', 'High', 'Low', 'Close', 'Volume', 'Date', 'Symbol']
TRAIN_COLS = ['Open', 'High', 'Low', 'Close', 'Volume']
df_cache = df_cache[COLUMNS]
df_ticker_cache = df_cache['Symbol'].unique()


def get_ticker(stock):
    ticker = yf.Ticker(stock)
    return ticker


def validate_dt(date_text):
    if not date_text:
        return None
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        print("Incorrect data format, should be YYYY-MM-DD not ", date_text)
        return None
    return date_text


def get_6m_date_interval():
    delta = timedelta(days=240)
    today = datetime.datetime.now() - timedelta(days=1)
    return datetime.datetime.strftime(today - delta, '%Y-%m-%d'), \
           datetime.datetime.strftime(today, '%Y-%m-%d'),


def update_cache(df, stock_name):

    if len(df) == 0:
        return
    df['Symbol'] = stock_name
    if 'Date' not in df.columns:
        df.reset_index(inplace=True)
        df['Date'] = df['Date'].apply(lambda dt: dt[:10])
    print(df)
    pd.concat([df_cache, df[COLUMNS]], ignore_index=True)
    df_cache.to_csv(STACK_CACHE_PATH, index=False)


@lru_cache(5)
def get_historical(stock, interval='1d', st_dt=None, ed_dt=None):
    if not validate_dt(st_dt) or not validate_dt(ed_dt):
        st_dt, ed_dt = get_6m_date_interval()

    if interval not in INTERVALS:
        interval = '1d'

    # try:
    #     # If stock is present in cache
    #     if stock in df_ticker_cache:
    #         stock_df_cache = df_cache[df_cache['Symbol'] == stock][['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
    #         # if stock data is present till start date
    #         if min(stock_df_cache['Date']) <= st_dt:
    #             if max(stock_df_cache['Date']) >= ed_dt:
    #                 historical = stock_df_cache[(stock_df_cache.Date > st_dt) & (stock_df_cache.Date < ed_dt)]
    #                 return historical.set_index('Date')
    #             else:
    #                 historical1 = stock_df_cache[(stock_df_cache.Date > st_dt)].set_index('Date')[TRAIN_COLS]
    #                 tick = get_ticker(stock)
    #                 historical = tick.history(start=max(stock_df_cache['Date']), end=ed_dt, interval=interval)
    #                 update_cache(historical, stock)
    #                 return pd.concat([historical1, historical[COLUMNS]]).set_index('Date')
    # except Exception as e:
    #     print(e)
    #     print(traceback.format_exc())
    #     raise e

    tick = get_ticker(stock)
    historical = tick.history(start=st_dt, end=ed_dt, interval=interval)
    # ['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits'],
    return historical


if __name__ == '__main__':
    df = get_historical('GOOG')
    df.to_csv('test_case_files/GOOG.csv')
