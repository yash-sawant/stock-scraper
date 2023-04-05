import pandas as pd
import os
import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from keras.models import load_model
import tensorflow as tf

# Loading model
MODEL_FOLDER = 'model/model_150_v2'
model = load_model(MODEL_FOLDER)

# MODEL_FOLDER = 'model/model_v1'
# model = load_model(MODEL_FOLDER)

TRAIN_COLS = ['Open', 'High', 'Low', 'Close', 'Volume']
INPUT_SIZE = 120
OUTPUT_SIZE = 20


def extract_model_input(df):
    assert len(df) >= INPUT_SIZE
    return df[TRAIN_COLS].iloc[-INPUT_SIZE:, :]


def normalize_minmax(arr):
    """
    Normalize a numpy array using min-max scaling
    :param arr: numpy array to be normalized
    :return: normalized numpy array
    """
    arr_min = arr.min()
    arr_max = arr.max()
    return (arr - arr_min) / (arr_max - arr_min), (arr_min, arr_max)


def inverse_normalize(arr, scalar):
    arr_min, arr_max = scalar
    return arr * (arr_max - arr_min) + arr_min


def dt_func(dt):
    return datetime.datetime.strptime(dt[:10], "%Y-%m-%d")


def predict(df):
    scalars = {}
    x = extract_model_input(df)

    for col in TRAIN_COLS:
        arr = x[col].values
        x[col], scalar = normalize_minmax(arr)
        scalars[col] = scalar

    x_in = x.values.reshape((1, *x.shape))
    pred = model.predict(x_in)

    pred = inverse_normalize(pred.flatten(), scalars['Close'])

    return pd.DataFrame({'Close': pred})


def evaluate(df):
    lookback = INPUT_SIZE + OUTPUT_SIZE
    X_test = df.iloc[-lookback:-OUTPUT_SIZE]
    y_test = df.iloc[-OUTPUT_SIZE:]
    print(X_test.iloc[-1,:])
    print(y_test.iloc[-1,:])
    scalars = {}
    x = X_test[TRAIN_COLS]

    for col in TRAIN_COLS:
        arr = x[col].values
        x[col], scalar = normalize_minmax(arr)
        scalars[col] = scalar

    x_in = x.values.reshape((1, *x.shape))
    pred = model.predict(x_in)
    pred = inverse_normalize(pred.flatten(), scalars['Close'])

    return pd.DataFrame({'Date': y_test.index, 'Close': pred}).set_index('Date'), \
           pd.DataFrame({'Date': y_test.index, 'Close': y_test['Close']}).set_index('Date')


if __name__ == "__main__":
    from stock_info import get_historical

    df = get_historical('GOOG')
    print(df.head(1))
    print(df.shape)
    print(df.columns)
    # print(predict(df))
    print(evaluate(df))
