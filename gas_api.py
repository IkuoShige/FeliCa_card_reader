import requests
import json

def send_GAS_API(value):
    # GASのWebアプリURL
    url = 'https://script.google.com/macros/s/AKfycbygWD_tB3sYw4LvjzLmx8IUMvtcxpnHVU84l7dn5hL68guI2DzQCDhepjVBNK6Hf6XjwA/exec'

    # 送信データ
    data = {
        "data": [value]
    }

    # POSTリクエストを送信
    response = requests.post(url, json=data)

    # レスポンスを表示
    print(response)

