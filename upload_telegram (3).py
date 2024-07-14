import os
import telebot
from telebot import types
from dotenv import load_dotenv
from currency_converter import CurrencyConverter

amount_of_currency = 0
currency = CurrencyConverter()
tg_token = os.environ["TG_TOKEN"]
bot = telebot.TeleBot(tg_token)


@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(
        message.chat.id,
        "Здравствуйте, {0.first_name}! Я чат-бот🤖. С моей помощью вы можете конвертировать валюты. Введите сумму, которую вы хотите конвертировать: "
        .format(message.from_user))
    bot.register_next_step_handler(message, entering_the_amount)


def entering_the_amount(message):
    global amount_of_currency
    try:
        amount_of_currency = float(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат. Введите сумму")
        bot.register_next_step_handler(message, entering_the_amount)
        return

    if amount_of_currency > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        button1 = types.InlineKeyboardButton("USD/EUR",
                                             callback_data="USD/EUR")
        button2 = types.InlineKeyboardButton("RUB/USD",
                                             callback_data="RUB/USD")
        button3 = types.InlineKeyboardButton("USD/JPY",
                                             callback_data="JPY/USD")
        button4 = types.InlineKeyboardButton("GBP/USD",
                                             callback_data="GBP/USD")
        button5 = types.InlineKeyboardButton("Другая пара",
                                             callback_data="else")
        markup.add(button1, button2, button3, button4, button5)
        bot.send_message(message.chat.id,
                         "<b>Выберите пару валют</b>💵: ",
                         parse_mode="HTML",
                         reply_markup=markup)
    else:
        bot.send_message(message.chat.id,
                         "Сумма должна быть больше нуля. Введите сумму")
        bot.register_next_step_handler(message, entering_the_amount)


@bot.callback_query_handler(func=lambda _: True)
def callback_data(call):
    if call.data != "else":
        values = call.data.split("/")
        converted_value = currency.convert(amount_of_currency, values[0],
                                           values[1])
        bot.send_message(
            call.message.chat.id,
            f"Результат конвертирования: <u>{round(converted_value, 2)}</u>. Можете заново вписать сумму",
            parse_mode="HTML")
        bot.register_next_step_handler(call.message, entering_the_amount)
    else:
        bot.send_message(call.message.chat.id, "Введите пару валют через: /")
        bot.register_next_step_handler(call.message, entering_my_currencies)


def entering_my_currencies(message):
    try:
        values = message.text.upper().split("/")
        converted_value = currency.convert(amount_of_currency, values[0],
                                           values[1])
        bot.send_message(
            message.chat.id,
            f"Результат конвертирования: <u>{round(converted_value, 2)}</u>. Можете заново вписать сумму",
            parse_mode="HTML")
        bot.register_next_step_handler(message, entering_the_amount)
    except Exception:
        bot.send_message(message.chat.id,
                         "Что-то не так. Введите пару валют заново")
        bot.register_next_step_handler(message, entering_my_currencies)


def main():
    load_dotenv()
    bot.infinity_polling()


if __name__ == "__main__":
    main()
