# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import config
#from time import time
import time
import telebot
from telebot import types
import requests
from aiohttp import web
import ssl


bot = telebot.TeleBot(config.TOKEN)

# https://api.telegram.org/bot<token>/sendMessage?chat_id=<chat_id>&text=<Enter your text here>
# https://api.thecatapi.com/v1/images/search?mime_type=jpg     #картинки с котиками.

@bot.message_handler(commands=['start'])  # работает
def handler_start(message):
    user_markup = types.ReplyKeyboardMarkup(True)
    user_markup.row('Переводчик', 'Контакты', 'Убрать кнопки')
    bot.send_message(message.from_user.id, 'Привет, я Genesis-бот', reply_markup=user_markup)
    # bot.forward_message(chat_id=271249491, from_chat_id=message.chat.id, message_id=message.message_id)  # пересылка мессаги


# @bot.message_handler(commands=['stop'])
# def handler_stop(message):
#     hide_keyboard = types.ReplyKeyboardRemove()
#     bot.send_message(message.from_user.id, reply_markup=hide_keyboard)


@bot.message_handler(commands=['help'])  # работает
def handler_help(message):
    bot.send_message(message.chat.id, 'Нужна помощь?')
    # bot.reply_to(message, 'Чем могу помочь?')


@bot.message_handler(commands=['about'])  # работает
def handler_about(message):
    bot.send_message(message.chat.id, 'Меня создали в Кибердайн Систем, теперь я твой помощник в этом цифровом мире.')


@bot.message_handler(commands=['contact'])  # работает
def send_contact(message):
    # bot.send_contact(message.chat.id, request_contact=True)
    bot.send_contact(message.chat.id, phone_number='03', first_name='request_contact=True')


@bot.message_handler(commands=['location'])  # работает
def send_location(message):
    bot.send_location(message.chat.id, latitude=48.858252, longitude=2.294489)
    # bot.send_message(message.chat.id, latitude, longitude, request_location=True)
    print(message.location)


@bot.message_handler(commands=['sticker'])  # работает
def send_sticker(message):
    # bot.send_sticker(message.chat.id, 'CAADAgADCAsAAi8P8AZv5AABGV_1eF8WBA')
    bot.send_sticker(message.chat.id, 'CAADAgADRAADq1fEC1nUzBZy6Z-0FgQ')


@bot.message_handler(commands=['photo'])  # работает
def send_photo(message):
    bot.send_photo(message.chat.id, 'AgADBAADBqsxGwAB0u1Qno0sRRL27S7A0yAbAAQBAAMCAAN4AAPrGwMAARYE')


@bot.message_handler(commands=['video'])
def sand_video(message):
    bot.send_video(message.chat.id, message.video.file_id)


@bot.message_handler(commands=['audio'])
def send_audio(message):
    bot.send_audio(message.chat.id, file_id)


@bot.message_handler(content_types=['document'])
def send_doc(message):
    bot.send_document(message.chat.id, file_id)

# @bot.message_handler(commands=['location'])  хз, может работать
# def handler_location(message):
#     print(message.location)

# dispatcher.add_handler(MessageHandler(Filters.location, location))  вроде рабочий вариант
# def location(bot, update):
#     print(update.message.location)


@bot.message_handler(commands=['geophone'])  # работает
def geophone(message):
    # keyboard = types.ReplyKeyboardMarkup(row_widht=1, resize_keyboard=True)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button_phone = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
    button_geo = types.KeyboardButton(text='Отправить геолокацию', request_location=True)
    keyboard.add(button_phone, button_geo)
    bot.send_message(message.from_user.id, 'Для заказа сообщи, пожалуйста, свой номер телефона', reply_markup=keyboard)
    # keyboard.row('Дай номер телефончега') другой способ, просто кнопка с текстом
    # bot.send_message(message.from_user.id, "message.text", reply_markup=keyboard)

# @bot.message_handler(content_types=["text"]) # работает
# def repeat_all_messages(message):
#     #bot.reply_to(message, message.text)
#     #bot.send_message(message.from_user.id, message.text) # надо пробануть
#     bot.send_message(message.chat.id, message.text)


# @bot.message_handler(content_types=["text"])  # работает
# def handler_message(message):
#     # bot.send_message(message.chat.id, message.text)
#     json = translate_me(message.text)
#     bot.send_message(message.chat.id, ''.join(json['text']))

# @bot.message_handler(commands=['convert'])  # работает, Реплай Клава
# def convert(message):
#     # keyboard = types.ReplyKeyboardMarkup(True, row_width=1)
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
#     button1 = types.KeyboardButton(text='Хочу перевести рубли в доллары')
#     button2 = types.KeyboardButton(text='Хочу перевести доллары в рубли')
#     keyboard.add(button1)
#     keyboard.add(button2)
#     # keyboard.add(button2)
#     bot.send_message(message.chat.id, 'Что будем делать?', reply_markup=keyboard)


@bot.message_handler(commands=['cat'])
def getcat(message):
    keyboard = types.ReplyKeyboardMarkup(True, False)
    keyboard.row('Получить котика')
    bot.send_message(message.chat.id, 'Привет! Нажми кнопарик ниже.', reply_markup=keyboard)


@bot.message_handler(regexp="Получить котика")
def  cat(message):
    # картинки с котиками
    url = 'https://api.thecatapi.com/v1/images/search?mime_type=jpg'
    res = requests.get(url)
    data = res.json()
    cat = data[0]['url']

    bot.send_photo(message.chat.id, cat)


@bot.message_handler(commands=['convert'])  # работает, Инлайн Клава
def convert(message):
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text='Sinobi', url='http://google.com')
    button2 = types.InlineKeyboardButton(text='Robisho', url='t.me/Robish0')
    keyboard.add(button1, button2)
    bot.send_message(message.chat.id, 'Кому будем писать?', reply_markup=keyboard)


@bot.message_handler(content_types=["text"])
def text(message):
    if message.text == 'Хочу перевести рубли в доллары':
        bsm = bot.send_message(message.chat.id, 'Сколько рублей хотите перевести?')
        bot.register_next_step_handler(bsm, next_usd)
    elif message.text == 'Хочу перевести доллары в рубли':
        bsm = bot.send_message(message.chat.id, 'Сколько долларов хотите перевести?')
        bot.register_next_step_handler(bsm, next_rub)
    elif message.text == 'Контакты':
        bot.send_message(message.from_user.id, 'Наши контакты очень известны')
    elif message.text == 'Переводчик':
        bot.send_message(message.from_user.id, 'Это функция-транслейтер', )
    elif message.text == 'Убрать кнопки':
        # keyboard = types.ReplyKeyboardMarkup(True)
        # bot.send_message(message.from_user.id, 'Теперь без кнопок', reply_markup=keyboard)
        hide_keyboard = types.ReplyKeyboardRemove()
        bot.send_message(message.from_user.id, '*', reply_markup=hide_keyboard)
    else:
        json = translate_me(message.text)  # перевод введенного текста
        bot.send_message(message.chat.id, ''.join(json['text']))


def  next_rub(message):
    bot.send_message(message.chat.id, 'Сумма в рублях: ' + str(int(message.text) * rate()))


def next_usd(message):
    bot.send_message(message.chat.id, 'Сумма в доларах: ' + str(int(message.text) / rate()))


def rate():  # курс руб к баксу
    url = 'https://api.exchangerate-api.com/v4/latest/USD'
    res = requests.get(url).json()
    return float(res['rates']['RUB'])
    # bot.send_message(message.chat.id, 'Сумма:', + message.text)


def translate_me(my_text):  # перевод текста
    params = {
        'key': config.ya_api_key,
        'text': my_text,
        'lang': 'ru-en'  # с какого языка на какой будем переводить
    }
    response = requests.get(config.ya_api_url, params=params)
    return response.json()


@bot.message_handler(commands=["reg"])
def start (message):
    keyboard = types.InlineKeyboardMarkup()
    but_1 = types.InlineKeyboardButton(text="Зарегестрироваться", callback_data="register")
    keyboard.add(but_1)
    bot.send_message(message.chat.id, "Добро пожаловать!", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "register":
            bot.send_message(call.message.chat.id, "Вы были зарегестрированы!")


# @bot.message_handler(content_types=["text"])  # работает
# def handler_message(message):
#     if message.text == 'Контакты':
#         bot.send_message(message.from_user.id, 'Наши контакты очень известны')
#     elif message.text == 'Переводчик':
#         bot.send_message(message.from_user.id, 'Это фунция транслейтер', )
#     elif message.text == 'Убрать кнопки':
#         # keyboard = types.ReplyKeyboardMarkup(True)
#         # bot.send_message(message.from_user.id, 'Теперь без кнопок', reply_markup=keyboard)
#         hide_keyboard = types.ReplyKeyboardRemove()
#         bot.send_message(message.from_user.id, '*', reply_markup=hide_keyboard)
#     else:
#         json = translate_me(message.text)  # перевод введенного текста
#         bot.send_message(message.chat.id, ''.join(json['text']))


# if __name__ == '__main__':
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as ex:
        print(ex)
        time.sleep(10)

    # bot.polling(none_stop=True)
    # bot.polling()  # тоже работает

# bot.polling(none_stop=True)
