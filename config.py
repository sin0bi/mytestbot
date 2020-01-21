# -*- coding: UTF-8 -*-
# !/usr/bin/env python3


TOKEN = '624087861:AAESIOy8BfQM7_y_L-Pz4yXV0g7XymMf9B8'

ya_api_key = 'trnsl.1.1.20200114T122528Z.9518dde06972a91e.1472c16a51ae10a6e5984963fffc97d9b30d90af'
ya_api_url = "https://translate.yandex.net/api/v1.5/tr.json/translate"  # адрес для обращения к апи

host = 'server ip'
port = 80  # 443, 80, 88 или 8443 (порт должен быть открыт!)

listen = '0.0.0.0'  # На некоторых серверах придется указывать такой же IP, что и host

cert = 'webhook_cert.pem'  # сертификат сервера
pkey = 'webhook_pkey.pem'  # приватный ключ сервера
