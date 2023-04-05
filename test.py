import pandas as pd
import datetime

df = pd.read_csv('database.csv')
x = df.iloc[0]['datetime']
dt_str = lambda x: datetime.datetime.strftime(datetime.datetime.fromisoformat(x), '%b %d, %Y, %H:%M %Z')

print(dt_str(x))


# articles = [(row[0], row[1], row[2], dt_str(row[3])) for i, row in df.iterrows()]
# print(articles[0])