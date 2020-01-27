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


@bot.message_handler(commands=['start'])  # работает
def handler_start(message):
    user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    user_markup.row('Переводчик', 'Конвертер', 'Котопёсики')
    bot.send_message(message.from_user.id, 'Привет, {0.first_name}!\nЯ Genesis-бот. Я многое уже умею, например, я могу перевести любую фразу с русского на английский, могу конвертировать руб/usd, могу выдать картинки с котикаме и пёсикаме'.format(message.from_user), reply_markup=user_markup)


@bot.message_handler(commands=['help'])  # работает
def handler_help(message):
    bot.send_message(message.chat.id, 'Нужна помощь?')


@bot.message_handler(commands=['about'])  # работает
def handler_about(message):
    bot.send_message(message.chat.id, 'Меня создали в Кибердайн Систем, теперь я буду следить за тобой всегда!')


@bot.message_handler(commands=['contact'])  # работает
def send_contact(message):
    # bot.send_contact(message.chat.id, request_contact=True)
    bot.send_contact(message.chat.id, phone_number='03', first_name='mynameisbot')


@bot.message_handler(commands=['location'])  # работает
def send_location(message):
    bot.send_location(message.chat.id, latitude=48.858252, longitude=2.294489)
    print(message.location)


@bot.message_handler(commands=['sticker'])  # работает
def send_sticker(message):
    bot.send_sticker(message.chat.id, 'CAADAgADCAsAAi8P8AZv5AABGV_1eF8WBA')
    # bot.send_sticker(message.chat.id, 'CAADAgADRAADq1fEC1nUzBZy6Z-0FgQ')


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


@bot.message_handler(commands=['geophone'])  # работает
def geophone(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button_phone = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
    button_geo = types.KeyboardButton(text='Отправить геолокацию', request_location=True)
    keyboard.add(button_phone, button_geo)
    bot.send_message(message.from_user.id, 'Для заказа сообщи, пожалуйста, свой номер телефона', reply_markup=keyboard)


@bot.message_handler(commands=['convert'])  # работает, ReplyKeyboard
def convert(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button1 = types.KeyboardButton(text='Хочу перевести рубли в доллары')
    button2 = types.KeyboardButton(text='Хочу перевести доллары в рубли')
    keyboard.add(button1)
    keyboard.add(button2)
    bot.send_message(message.chat.id, 'Что будем делать?', reply_markup=keyboard)


@bot.message_handler(commands=['cat'])
def getcat(message):
    keyboard = types.ReplyKeyboardMarkup(True, True)
    keyboard.row('Получить котика')
    bot.send_message(message.chat.id, 'Нажми кнопарик ниже', reply_markup=keyboard)


@bot.message_handler(regexp="Получить котика")
def  cat(message):
    # картинки с котиками
    url = 'https://api.thecatapi.com/v1/images/search?mime_type=jpg'
    res = requests.get(url)
    data = res.json()
    cat = data[0]['url']
    bot.send_photo(message.chat.id, cat)


@bot.message_handler(commands=['dog'])
def getdog(message):
    keyboard = types.ReplyKeyboardMarkup(True, True)
    keyboard.row('Получить пёсика')
    bot.send_message(message.chat.id, 'Нажми кнопочку ниже', reply_markup=keyboard)


@bot.message_handler(regexp="Получить пёсика")
def dog(message):
    # картинки с собачками
    url = 'https://api.thedogapi.com/v1/images/search?mime_type=jpg'
    res = requests.get(url)
    data = res.json()
    dog = data[0]['url']
    bot.send_photo(message.chat.id, dog)


@bot.message_handler(content_types=["text"])
def text(message):
    if message.text == 'Хочу перевести рубли в доллары':
        bsm = bot.send_message(message.chat.id, 'Сколько рублей хотите перевести?')
        bot.register_next_step_handler(bsm, next_usd)
    elif message.text == 'Хочу перевести доллары в рубли':
        bsm = bot.send_message(message.chat.id, 'Сколько долларов хотите перевести?')
        bot.register_next_step_handler(bsm, next_rub)
    elif message.text == 'Конвертер':
        bot.send_message(message.from_user.id, 'Командой /convert можете начать конвертацию')
    elif message.text == 'Переводчик':
        bot.send_message(message.from_user.id, 'Это функция-транслейтер, напишите какую-нибудь фразу на русском языке и я переведу это на английский')
    elif message.text == 'Котопёсики':
        # keyboard = types.ReplyKeyboardMarkup(True)
        # bot.send_message(message.from_user.id, 'Теперь без кнопок', reply_markup=keyboard)
        # hide_keyboard = types.ReplyKeyboardRemove()
        bot.send_message(message.from_user.id, text='Выберите котика командой /cat или пёсика командой /dog')
    else:
        json = translate_me(message.text)  # перевод введенного текста
        bot.send_message(message.chat.id, '__pycache__/'.join(json['text']))


def  next_rub(message):
    bot.send_message(message.chat.id, 'Сумма в рублях: ' + str(float(message.text) * rate()))


def next_usd(message):
    bot.send_message(message.chat.id, 'Сумма в доларах: ' + str(float(message.text) / rate()))


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


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as ex:
            print(ex)
            time.sleep(10)
