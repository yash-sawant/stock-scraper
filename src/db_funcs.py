import sqlite3
import datetime
from datetime import timedelta
import pandas as pd
from web_scraping import get_new_articles
from collections import defaultdict

DATABASE_GENERATED = False
DB_FILE_NAME = 'database.csv'

def read_sql():
    pass


def get_last_update_dt():
    curr_dt = datetime.datetime.now()
    if DATABASE_GENERATED:
        df = pd.read_csv(DB_FILE_NAME)
        res_dt = df.iloc[-1]['datetime']
    else:
        res_dt = curr_dt - timedelta(days=14)
        res_dt = datetime.datetime(day=res_dt.day, year=res_dt.year, month=res_dt.month)
    return res_dt

    ### Read from db and get latest datapoint


def convert_to_dataframe(data):
    df_dict = defaultdict(list)
    for row in data:
        df_dict['source'].append(row[0])
        df_dict['title'].append(row[1])
        df_dict['article_brief'].append(row[2])
        df_dict['datetime'].append(row[3])
    return pd.DataFrame(df_dict)


def load_database():
    db = pd.read_csv(DB_FILE_NAME)
    return db


def refresh_database():
    global DATABASE_GENERATED
    last_time = get_last_update_dt()
    print('Loading news article since ',last_time.isoformat())
    data = get_new_articles(last_time)
    df = convert_to_dataframe(data)
    if DATABASE_GENERATED:
        print('Updating database')
        db = pd.read_csv(DB_FILE_NAME)
        db.append(df)
    else:
        print('Creating database')
        df.to_csv(DB_FILE_NAME, index=False)

    DATABASE_GENERATED = True
    return df

def write_sql():
    pass


def create_sql():
    pass
