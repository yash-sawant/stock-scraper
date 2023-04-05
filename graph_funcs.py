import matplotlib
matplotlib.use('agg')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from matplotlib.figure import Figure

from stock_info import get_historical

PRED_SIZE = 20


def get_candlestick(df, title='', pred=None, eval=None):
    fig = plt.figure(figsize=(20, 10))

    if 'Date' in df.columns:
        df.set_index('Date', inplace=True)

    df.index = pd.to_datetime(df.index)

    if eval is not None:
        df = df.iloc[:-len(eval),:]

    # define width of candlestick elements
    width = 1
    width2 = .07

    # define up and down df
    up = df[df.Close >= df.Open]
    down = df[df.Close < df.Open]

    # define colors to use
    col1 = 'green'
    col2 = 'red'
    col3 = 'blue'
    col4 = 'black'

    # plot up df
    plt.bar(up.index, up.Close - up.Open, width, bottom=up.Open, color=col1)
    plt.bar(up.index, up.High - up.Close, width2, bottom=up.Close, color=col1)
    plt.bar(up.index, up.Low - up.Open, width2, bottom=up.Open, color=col1)

    # plot down df
    plt.bar(down.index, down.Close - down.Open, width, bottom=down.Open, color=col2)
    plt.bar(down.index, down.High - down.Open, width2, bottom=down.Open, color=col2)
    plt.bar(down.index, down.Low - down.Close, width2, bottom=down.Close, color=col2)

    if pred is not None:
        last_close = df.Close.iloc[-1]
        pred_close = np.insert(pred.Close.values, 0, last_close)
        dates = pd.date_range(max(df.index), periods=PRED_SIZE + 1, freq='D')
        plt.plot(dates, pred_close, color=col3)

    if eval is not None:
        last_close = df.Close.iloc[-1]
        eval_close = np.insert(eval.Close.values, 0, last_close)
        dates = pd.date_range(max(df.index), periods=PRED_SIZE + 1, freq='D')
        plt.plot(dates, eval_close, color=col4)

    # ax2 = plt.twinx()
    # plt.bar(df.index,df.Volume,color='light blue',ax=ax2, alpha=0.3)

    # rotate x-axis tick labels
    plt.xticks(rotation=45, ha='right')
    plt.grid()
    plt.tight_layout()
    # plt.title(title)

    # #display candlestick chart
    # plt.show()
    return fig


def fig_2_img(fig):
    '''
    Converts matplotlib figure to a static image
    :param fig: Matplotlib figure
    :return:
    '''
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    fig.clf()
    return data


def plot_single_graph(stock_name, data, pred=None):
    '''
    Renders graph for given stock
    :param stock_name: name of stock
    :return: webpage
    '''

    if pred is not None:
        title = f"{stock_name} - Last 6 months + 20 Day prediction"
        content = [(fig_2_img(get_candlestick(data, title=title, pred=pred)), title)]
    else:
        title = f"{stock_name} - Last 6 months"
        content = [(fig_2_img(get_candlestick(data, title=title)), title)]
    return content


def plot_eval_graph(stock_name, df, pred, true):
    title = f"{stock_name} - Last 6 months with 20 days of prediction and 20 days of actual closing values"

    content = [(fig_2_img(get_candlestick(df, title=title, pred=pred, eval=true)), title)]

    return content


if __name__ == "__main__":
    # df = pd.read_csv('test_case_files/goog_6m.csv')
    # pred = pd.read_csv('test_case_files/pred_goog_6m.csv')
    # fig = get_candlestick(df, pred=pred)
    #
    # fig.savefig('test_case_files/goog.png', format="png")
    import os

    os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
    from stock_info import get_historical
    from prediction import predict

    df = get_historical('GOOG')
    # df = pd.read_csv('test_case_files/GOOG.csv')
    pred = predict(df)
    fig = get_candlestick(df, pred=pred)
    fig.savefig('test_case_files/goog.png', format="png")
