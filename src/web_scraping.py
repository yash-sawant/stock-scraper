import bs4
from bs4 import BeautifulSoup as soup
import csv
import pandas as pd
from urllib.request import Request, urlopen
import datetime
from datetime import timedelta

URL_BASE = 'https://www.prnewswire.com/news-releases/news-releases-list/?month={}&day={}&year={}&hour={}&page={}&pagesize={}'


def get_page_html(URL):
    req = Request(
        url=URL,
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    webpage = urlopen(req).read()
    html = soup(webpage, features="lxml")
    return html


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


def extract_news_from_page(html):
    headlines = html.find_all("div", "row arabiclistingcards")
    result = []
    for hd in headlines:
        src = hd.a.attrs['href']
        head = hd.h3.text#.split('\n')[3]
        article = hd.p.text
        time_pb = hd.h3.small.text
        dt_obj = validate_prn_date_time(time_pb)
        result.append((src, head, article, dt_obj))
    return result


def get_new_articles(since: datetime.datetime = None, PAGES=False):
    URL = URL_BASE.format(since.month, since.day, since.year, since.hour, 1, 100)
    html = get_page_html(URL)
    results = extract_news_from_page(html)
    if PAGES:
        page_nums = html.find_all('ul', 'pagination')[0].find_all('a')
        pages = []
        for pg in page_nums:
            try:
                pg_nm = int(pg['text'])
                pages.append(pg_nm)
            except Exception as e:
                continue
        for pg in pages:
            URL = URL_BASE.format(since.month, since.day, since.year, since.hour, pg, 100)
            html = get_page_html(URL)
            results.extend(extract_news_from_page(html))
    return results


def get_stock_news(stock_name):
    finviz_url = 'https://finviz.com/quote.ashx?t='
    news_tables = {}
    url = finviz_url + stock_name
    req = Request(url=url, headers={'User-Agent': 'Mozilla/5.0'})
    resp = urlopen(req)
    html = soup(resp, features="lxml")
    news_table = html.find(id='news-table')
    news_tables[stock_name] = news_table
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


def get_ticker():
    pass


if __name__ == '__main__':
    # get_new_articles()
    # get_stock_news('AAPL')
    pass
