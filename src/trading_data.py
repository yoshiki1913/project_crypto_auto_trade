from config.config import *
import pandas as pd
import ccxt

class TradingData:

    __bitmex = ccxt.bitmex({"apiKey": API_KEY, "secret": API_SERCRET})

    def get_past_data(self, period, bar):
        candles = []
        timest = self.__bitmex.fetch_ticker('BTC/USD')['timestamp']

        period += 1

        timest = timest - period * bar * 60 * 1000

        candles = self.__bitmex.fetch_ohlcv('BTC/USD', timeframe='1m', since=timest)

        pd_candles = pd.DataFrame(candles)

        return pd_candles