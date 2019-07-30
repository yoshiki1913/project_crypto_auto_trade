import numpy as np
import pandas as pd

class TechniqueAnalysis:

    def ema(self, period, minute_ago_data, close, data_n):
        """Form a complex number.

        Keyword arguments:
        period -- the real part (default 0.0)
        minute_ago_data -- the imaginary part (default 0.0)
        """
        ema_data = []

        for i in range(2 * period):
            ema_data.insert(0, close[data_n - 1 - i])

        if minute_ago_data == 0:
            arr = np.array(ema_data)[-period:]
        else:
            arr = np.array(ema_data)[-minute_ago_data - period:-minute_ago_data]

        ema = pd.Series(arr).ewm(span=period).mean()
        # print("EMA: {}".format(str(ema)))
        return ema[period - 1]

    def rsi(self, p, close):
        rsi_priod = p
        diff = close.diff(1)

        positive = diff.clip(lower=0).ewm(alpha=1.0 / rsi_priod).mean()
        nagative = diff.clip(upper=0).ewm(alpha=1.0 / rsi_priod).mean()

        result = 100 - 100 / (1 - positive / nagative)

        return result

    def macd_signal(self, short_term, long_term, signal_period, close, data_n):
        macd = []
        for i in range(short_term):
            macd.insert(0, self.ema(short_term, i, close, data_n) - self.ema(long_term, i, close, data_n))
        arr = np.array(macd)[-signal_period:]
        signal = pd.Series(arr).rolling(signal_period).mean()

        return macd, signal

    def atr(self, period, past_data, data_n):
        data = []
        for i in range(2 * period - 1):
            # 当日高値 - 当日安値
            p1 = past_data[2][data_n - i - 1] - past_data[3][data_n - i - 1]
            # 当日高値 - 前日安値
            p2 = past_data[2][data_n - i - 1] - past_data[4][data_n - i - 2]
            # 当日安値 - 前日終値
            p3 = past_data[2][data_n - i - 1] - past_data[4][data_n - i - 2]

            tr = max(abs(p1), abs(p2), abs(p3))

            data.insert(0, tr)

            arr = np.array(data)[-period:]
            atr = pd.Series(arr).ewm(span=period).mean()

        return atr[period - 1]