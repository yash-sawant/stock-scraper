import bs4
from bs4 import BeautifulSoup as soup
import csv
import pandas as pd
from urllib.request import Request, urlopen
import datetime
from datetime import timedelta
from functools import lru_cache
from time import time

URL_BASE = 'https://www.prnewswire.com/news-releases/news-releases-list/?month={}&day={}&year={}&hour={}&page={}&pagesize={}'


def validate_prn_date_time(date_text):
    try:
        if ',' in date_text:
            dt_obj = datetime.datetime.strptime(date_text, '%b %d, %Y, %H:%M %Z')
        else:
            dt_obj = datetime.datetime.strptime(date_text, '%H:%M %Z')
            dt_obj = datetime.datetime.now().replace(hour=dt_obj.hour, minute=0)
    except Exception as e:
        dt_obj = datetime.datetime.now() - timedelta(days=1)
    return dt_obj


def get_page_html(URL):
    req = Request(
        url=URL,
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    webpage = urlopen(req).read()
    html = soup(webpage, features="lxml")
    return html


def extract_news_from_page(html):
    headlines = html.find_all("div", "row arabiclistingcards")
    result = []
    for hd in headlines:
        src = hd.a.attrs['href']
        head = hd.h3.text  # .split('\n')[3]
        article = hd.p.text
        time_pb = hd.h3.small.text
        dt_obj = validate_prn_date_time(time_pb)
        result.append((src, head, article, dt_obj))
    return result


@lru_cache()
def get_new_articles(since: datetime.datetime):
    results = []
    days = (datetime.datetime.now() - since).days
    for i in range(days):
        start_time = time()
        URL = URL_BASE.format(since.month, since.day, since.year, since.hour, 1, 100)
        html = get_page_html(URL)
        page_data = extract_news_from_page(html)
        results.extend(page_data)
        print('Downloaded data for {} in {} seconds'.format(since.date(), round(time() - start_time), 3))
        since = since + timedelta(days=1)
    return results


def get_stock_news(stock_name):
    '''
    Read stock specific news from finviz.com
    :param stock_name: name of stock
    :return: (url, article title, article text)
    '''
    finviz_url = 'https://finviz.com/quote.ashx?t='
    url = finviz_url + stock_name
    html = get_page_html(url)
    news_table = html.find(id='news-table')
    # print(news_table)
    df_tr = news_table.findAll('tr')

    result = []
    for i, table_row in enumerate(df_tr):
        a_text = table_row.a.text
        td_text = table_row.td.text
        src = table_row.a.attrs['href']
        td_text = td_text.strip()
        result.append((src, a_text, td_text))

    return result


if __name__ == '__main__':
    # get_new_articles()
    # get_stock_news('AAPL')
    pass
