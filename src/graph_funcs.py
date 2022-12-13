import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from functools import lru_cache
import seaborn as sb
import pandas as pd

# plt.set_cmap('jet')
# plt.rcParams['axes.facecolor'] = 'white'
# plt.style.use('dark_background')


def get_candlestick(df,title=''):

    fig = plt.figure(figsize=(20,10))

    #define width of candlestick elements
    width = 1
    width2 = .07

    #define up and down df
    up = df[df.Close>=df.Open]
    down = df[df.Close<df.Open]

    #define colors to use
    col1 = 'green'
    col2 = 'red'

    #plot up df
    plt.bar(up.index,up.Close-up.Open,width,bottom=up.Open,color=col1)
    plt.bar(up.index,up.High-up.Close,width2,bottom=up.Close,color=col1)
    plt.bar(up.index,up.Low-up.Open,width2,bottom=up.Open,color=col1)

    #plot down df
    plt.bar(down.index,down.Close-down.Open,width,bottom=down.Open,color=col2)
    plt.bar(down.index,down.High-down.Open,width2,bottom=down.Open,color=col2)
    plt.bar(down.index,down.Low-down.Close,width2,bottom=down.Close,color=col2)

    # ax2 = plt.twinx()
    # plt.bar(df.index,df.Volume,color='light blue',ax=ax2, alpha=0.3)

    #rotate x-axis tick labels
    plt.xticks(rotation=45, ha='right')
    plt.grid()
    plt.title(title)

    # #display candlestick chart
    # plt.show()

    return fig