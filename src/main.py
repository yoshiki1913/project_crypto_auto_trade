from src.technique_analysis import TechniqueAnalysis
from src.trading_signals import TradingSignals
from src.trading_data import TradingData
from config.config import *
from time import sleep
import ccxt
import datetime

if __name__ == '__main__' :

    analysis = TechniqueAnalysis()
    signal = TradingSignals()
    data = TradingData()

    flags = {
        'no_position': True,
        'have_position': False
    }

    settlement_price = {
        'qty': 0,
        'limit': 0,
        'stop': 0
    }

    bitmex = ccxt.bitmex({"apiKey": API_KEY, "secret": API_SERCRET})
    bitmex.urls['api'] = bitmex.urls['test']

    bitmex.private_post_position_leverage({"symbol": "XBTUSD", "leverage": str(LEVERAGE)})

    # 現在の保有数
    total_btc = bitmex.fetch_balance()['BTC']['total']

    # 何分足
    bar = 1
    # ロウソク足いくつ
    data_n = 60
    # 個数
    amount = 1500

    # 現在日時分
    get_time = datetime.datetime.today().minute
    #

    # 過去データ
    past_data = data.get_past_data(data_n, bar)
    close = past_data[4]

    BUY = 'Buy'
    SELL = 'Sell'

    # 保有ポジション
    position = bitmex.private_get_position()
    # 残高
    balance = bitmex.fetch_balance()
    #
    now_price = None
    #
    cnt = 0
    print('実行中')
    print("実行直後の残高:{}".format(total_btc))
    while (True):
        while (flags['no_position']):
            if datetime.datetime.today().minute % bar == 0:
                if get_time == datetime.datetime.today().minute:
                    cnt += 1
                    sleep(1)
                    break
                print('-----------------------------')
                now_time = datetime.datetime.now()
                print(str(now_time))
                print("同一時間繰り返し回数: {}".format(str(cnt)))
                cnt = 0


                past_data = data.get_past_data(data_n, bar)
                close = past_data[4]
                get_time = datetime.datetime.today().minute

                if close[data_n - 1] != now_price:
                    print("データの再取得 - done")
                    print("RSI: ", analysis.rsi(14, close)[data_n - 1])
                    print("MACD: ", analysis.macd_signal(12, 26, 9, close, data_n))
                    print("現在価格: ", close[data_n - 1])

                    now_price = close[data_n - 1]
                else:
                    print("{} == {}".format(str(close[data_n - 1]), str(now_price)))

            if signal.buy_signal(data_n, close):
                print("買い注文開始")
                print("ATR: " + str(int(analysis.atr(14, past_data, data_n))))

                width = int(2 * analysis.atr(14, past_data, data_n))
                price = bitmex.fetch_ticker("BTC/USD")["close"]

                settlement_price['qty'] = 1
                settlement_price['limit'] = price + width
                settlement_price['stop'] = price - width
                settlement_price['price'] = price

                buy = bitmex.create_order("BTC/USD", "market", "buy", amount)

                print('buy')
                print(settlement_price)

                flags['have_position'] = True
                flags['no_position'] = False

                position = bitmex.private_get_position()

            if signal.sell_signal(data_n, close):
                print("売り注文開始")
                print("ATR: " + str(int(analysis.atr(14, past_data, data_n))))

                width = int(2 * analysis.atr(14, past_data, data_n))
                price = bitmex.fetch_ticker("BTC/USD")["close"]

                settlement_price['qty'] = -1
                settlement_price['limit'] = price - width
                settlement_price['stop'] = price + width
                settlement_price['price'] = price

                sell = bitmex.create_order("BTC/USD", "market", "sell", amount)

                print('sell')
                print(settlement_price)

                flags['have_position'] = True
                flags['no_position'] = False

                position = bitmex.private_get_position()

        while (flags['have_position']):
            print('have_position')
            if signal.settlement_buy_signal(settlement_price):
                print('買い決済しました')
                settlement = bitmex.create_order("BTC/USD", "market", "buy", amount)

                print(settlement)

                balance = bitmex.fetch_balance()

                flags['have_position'] = False
                flags['no_position'] = True

                print("買い決済あとの残高:{}".format(total_btc))

            if signal.settlement_sell_signal(settlement_price):
                print('売り決済しました')
                settlement = bitmex.create_order("BTC/USD", "market", "sell", amount)

                print(settlement)

                balance = bitmex.fetch_balance()

                flags['have_position'] = False
                flags['no_position'] = True

                print("売り決済あとの残高:{}".format(total_btc))

            sleep(30)