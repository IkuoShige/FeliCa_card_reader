import requests
import json

def send_GAS_API(url, value):
    # GASのWebアプリURL
    # url = 'https://script.google.com/macros/s/AKfycbygWD_tB3sYw4LvjzLmx8IUMvtcxpnHVU84l7dn5hL68guI2DzQCDhepjVBNK6Hf6XjwA/exec'

    # 送信データ
    data = {
        "data": [value]
    }

    # POSTリクエストを送信
    response = requests.post(url, json=data)

    # レスポンスを表示
    # if response.status_code == 200:
        # print('データを送信しました')
    # print(response)
    return response

