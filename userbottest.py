from pyrogram import Client
from pyrogram.types import Message
from keys import api_key, secret_key, api_hash, api_id
import time
import requests
import hmac
import hashlib


app = Client("my_account")
client = Client(name='meclient', api_id=api_id, api_hash=api_hash)


def hashing(query_string):
    return hmac.new(secret_key.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()


@client.on_message()
def all_message(client: Client, message: Message):
    if message.chat.id == 6094219188: #от бота
        if 'Upped' in message.text:
            coin = message.text.split(" ")[0]
            side = 'Sell'
            print(f'Монета: {coin}, открываю шорт!')

            def make_market_order(order_type,
                                  qty,
                                  symbol=coin,
                                  side=side,
                                  category='linear',
                                  is_isolated=True):
                url = 'https://api.bybit.com/v5/order/create'
                current_time = int(time.time() * 1000)
                data = '{' + f'"symbol": "{symbol}", "side": "{side}", "is_isolated": "{is_isolated}", "orderType": "{order_type}", "qty": "{qty}", "category": "{category}"' + '}'
                sign = hashing(str(current_time) + api_key + '5000' + data)

                headers = {
                    'X-BAPI-API-KEY': api_key,
                    'X-BAPI-TIMESTAMP': str(current_time),
                    'X-BAPI-SIGN': sign,
                    'X-BAPI-RECV-WINDOW': str(5000)
                }

                response = requests.post(url=url, headers=headers, data=data)
                #print(response.text)

            make_market_order(order_type='Market', qty=1)


client.run()
