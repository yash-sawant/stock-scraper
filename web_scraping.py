import bs4
from bs4 import BeautifulSoup as soup
import csv
import pandas as pd
from urllib.request import Request, urlopen


def get_new_articles():
    # creating csv file
    # filename = 'newsHeadlines.csv'
    # f = open(filename, 'w', newline='')
    # music = csv.writer(f)

    URL = 'https://www.prnewswire.com/news-releases/news-releases-list/'

    req = Request(
        url=URL,
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    webpage = urlopen(req).read()
    bsobj = soup(webpage, features="html.parser")
    headlines = bsobj('span', {'class': 'langspan'})
    xl = []  # for excel Dataset

    for row in headlines:
        cols = [element.text.strip() for element in row]
        # music.writerow(cols)  # Writing to CSV
        xl.append(cols)
        print(cols)

    df = pd.DataFrame(data=xl[1:], columns=xl[0])
    df.to_csv('world_music.csv', index=False, header=False)


def get_stock_news(stock_name):
    pass


def get_ticker():
    pass


if __name__ == '__main__':
    get_new_articles()
