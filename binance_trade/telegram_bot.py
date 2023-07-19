import time

import talib

from telebot import TeleBot

from auth_telegram import token
from trade_bot_future import TradeBotFutures

bot = TeleBot(token=token)


@bot.message_handler(commands=['start'])
def greetings(message):
    bot.send_message(
        message.chat.id,
        f'<b>Привет</b>,    <em>{message.from_user.first_name} {message.from_user.last_name}</em>',
        # message,
        parse_mode='html'
    )
    bot.send_message(message.chat.id, 'Enter: /start_robot')


@bot.message_handler(commands=['start_robot'])
def start_alert(message):

    cfx = TradeBotFutures(symbol='CFXUSDT')
    cfx.start_bot()
    if cfx.state == 'BUY':
        bot.send_message(chat_id=message.chat.id, text=f'Совершена покупка CFX')
    elif cfx.state == 'Sell':
        bot.send_message(chat_id=message.chat.id, text=f'Совершена продажа CFX')


if __name__ == '__main__':
    bot.polling(none_stop=True)
