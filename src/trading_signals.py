from config.config import *
from .technique_analysis import TechniqueAnalysis
import ccxt

class TradingSignals:

    __bitmex = ccxt.bitmex({"apiKey": API_KEY, "secret": API_SERCRET})
    analysis = TechniqueAnalysis()

    def buy_signal(self, data_n, close):

        if self.analysis.rsi(14, close)[data_n - 1] < 30 and \
                abs(self.analysis.macd_signal(12, 26, 9, close, data_n)[0][8] - self.analysis.macd_signal(12, 26, 9, close, data_n)[1][8]) > 10:
            print("買いポジのRSI: " + str(self.analysis.rsi(14, close)[data_n - 1]))
            print("買いポジのMACD値: " + str(abs(self.analysis.macd_signal(12, 26, 9, close, data_n)[0][8] - self.analysis.macd_signal(12, 26, 9, close, data_n)[1][8])))
            return True
        else:
            return False

    def sell_signal(self, data_n, close):
        if self.analysis.rsi(14, close)[data_n - 1] > 70 and \
                abs(self.analysis.macd_signal(12, 26, 9, close, data_n)[0][8] - self.analysis.macd_signal(12, 26, 9, close, data_n)[1][8]) > 10:
            return True
        else:
            return False

    def settlement_buy_signal(self, settlement_price):
        if settlement_price['qty'] > 0:
            return False

        last_price = self.__bitmex.fetch_ticker("BTC/USD")["close"]

        if last_price < settlement_price["limit"]:
            return True
        elif last_price > settlement_price["stop"]:
            return True
        else:
            return False

    def settlement_sell_signal(self, settlement_price):
        if settlement_price['qty'] < 0:
            return False

        last_price = self.__bitmex.fetch_ticker("BTC/USD")["close"]

        if last_price > settlement_price["limit"]:
            return True
        elif last_price < settlement_price["stop"]:
            return True
        else:
            return False