import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import threading


def pandas_demo(data):

    glass = data['btc_usd']
    bids = glass['bids']
    asks = glass['asks']

    bids_prices = [round(price, 1) for price, volume in bids]
    bids_volumes = [volume for price, volume in bids]

    asks_prices = [round(price, 1) for price, volume in asks]
    asks_volumes = [volume for price, volume in asks]

    bids_df = pd.DataFrame(bids_volumes, index=bids_prices, columns=['volume'])
    print('Bids head')
    print(bids_df.head())

    asks_df = pd.DataFrame(asks_volumes, index=asks_prices, columns=['volume'])
    print('Asks tail')
    print(asks_df.tail())

    bids_plot = bids_df.iloc[0:25].plot.barh()
    bids_plot.set_xlabel('BTC')
    bids_plot.set_ylabel('$')
    bids_plot.set_title('Bids glass')

    asks_plot = asks_df.iloc[0:25].plot.barh()
    asks_plot.set_xlabel('BTC')
    asks_plot.set_ylabel('$')
    asks_plot.set_title('Asks glass')
    plt.show()
