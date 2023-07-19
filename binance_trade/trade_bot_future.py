import time

import numpy as np
import talib
from binance.um_futures import UMFutures

from config_binance_api import Secret_Key, API_Key


class TradeBotFutures:
    __api_secret = Secret_Key
    __api_key = API_Key

    def __init__(self, symbol='BTCUSDT', interval='1m', quant=23, limit=100):
        """
        :param symbol: название монеты
        :param interval: указание интервала
        :param limit: лимит свечей
        :param quant: количество монет
        """

        client = UMFutures(key=API_Key, secret=Secret_Key)
        self.symbol = symbol
        self.interval = interval
        self.quant = quant
        self.limit = limit
        self.client = client
        self.state = ''
        self.price = ''

    def _get_data(self):
        klines = self.client.klines(symbol=self.symbol, interval=self.interval, limit=self.limit)
        return_data = []
        for each in klines:
            return_data.append(float(each[4]))

        return np.array(return_data)

    def _create_my_order(self, order_type):
        order = self.client.new_order(
            symbol=self.symbol,
            side=order_type,
            type='MARKET',
            quantity=self.quant
        )
        return order

    def _place_order(self, order_type):
        if order_type == 'BUY':
            self._create_my_order(order_type=order_type)
            # print("____BUY_____")
            self.state = order_type
        elif order_type == 'SELL':
            self._create_my_order(order_type=order_type)
            # print("____SELL____")
            self.state = order_type

    def start_alert_bot(self):
        """
        Запускает бота только на оповещение
        :return: string
        """
        while True:
            closing_data = self._get_data()
            rsi = talib.RSI(closing_data, 7)[-1]
            print(rsi)

            if rsi <= 30:
                print(f"BUY!!!!")

            if rsi >= 70:
                print("SELL!!!!")
            time.sleep(2)

    def start_bot(self):
        """
        Запускает бота на открытие позиции
        :return:
        """
        # buy = true  если с позиции продажи  buy = false если с позиции купить
        buy = True
        # # sell = false  если с позиции продажи  sell = true если с позиции купить
        sell = False
        while True:
            closing_data = self._get_data()
            rsi = talib.RSI(closing_data, 7)[-1]
            print(round(rsi))
            # self.price = str(closing_data[-1][4])

            if rsi <= 30 and not buy:
                self._place_order(order_type='BUY')
                # print("BUY!!!!")
                buy = not buy
                sell = not sell

            elif rsi >= 70 and not sell:
                self._place_order(order_type='SELL')
                # print("SELL!!!!")
                buy = not buy
                sell = not sell
            time.sleep(2)


def main():
    cfx = TradeBotFutures(symbol='CFXUSDT', interval='1m')
    cfx.start_alert_bot()
    # cfx.start_bot()


if __name__ == '__main__':
    main()
