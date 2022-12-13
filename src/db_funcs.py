import sqlite3
import datetime
from datetime import timedelta
import pandas as pd
from web_scraping import get_new_articles
from collections import defaultdict
from functools import lru_cache
import os
from csv import DictWriter


DB_FILE_NAME = 'database.csv'
DATABASE_GENERATED = os.path.exists(DB_FILE_NAME)
DEFAULT_DATE_RETRIEVAL = 7


def read_sql():
    pass


def get_last_update_dt():

    curr_dt = datetime.datetime.now()
    if DATABASE_GENERATED:
        df = pd.read_csv(DB_FILE_NAME)
        res_dt = datetime.datetime.fromisoformat(df.iloc[0]['datetime'])
    else:
        res_dt = curr_dt - timedelta(days=DEFAULT_DATE_RETRIEVAL)
        res_dt = datetime.datetime(day=res_dt.day, year=res_dt.year, month=res_dt.month)
    return res_dt

    ### Read from db and get latest datapoint


def convert_to_dataframe(data):
    df_dict = defaultdict(list)
    try:
        for row in data:
            df_dict['source'].append(row[0])
            df_dict['title'].append(row[1])
            df_dict['article_brief'].append(row[2])
            df_dict['datetime'].append(row[3].isoformat())
    except Exception as e:
        print(row)
        raise e
    return pd.DataFrame(df_dict)


@lru_cache()
def load_database(last_n = 10):
    db = pd.read_csv(DB_FILE_NAME)
    return db.iloc[::-1].head(last_n)


def refresh_database():
    global DATABASE_GENERATED

    last_time = get_last_update_dt()
    print('Loading news article since ', last_time)
    data = get_new_articles(last_time)
    df = convert_to_dataframe(data)

    if DATABASE_GENERATED:
        print('Updating database')
        db = pd.read_csv(DB_FILE_NAME)
        db.append(df)
        df = db
    else:
        print('Creating database')

    df.sort_values(by='datetime',inplace=True)
    df.to_csv(DB_FILE_NAME, index=False)
    DATABASE_GENERATED = True
    return df


def write_sql():
    pass


def create_sql():
    pass
