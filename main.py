import os
import random
import vk_api
import datetime
import time
import json
from pprint import pprint

file_path = os.path.join(os.getcwd(), 'token_vk.txt')  # Токен запрятан в отдельный файл (token_vk.txt).
with open(file_path, 'r', encoding='utf-8') as f:
    token_vk = f.readline()
    # print(token_vk)
vk_session = vk_api.VkApi(token=token_vk)  # Создаем переменную сесии.
vk = vk_session.get_api()  # Создаем другую переменную (vk), где переменную сесии (vk_session) подключаем к api списку методов.
vk_session._auth_token()  # Авторизация токена.


def get_last_msg():
    messages = vk_session.method("messages.getConversations",
                                 {"offset": 0, "count": 100, "filter": "unanswered", "group_id": 218321292})
    # print(f'messages-  \n {messages}')
    text1 = messages['items'][0]
    text2 = messages['items'][0]['conversation']
    text3 = messages['items'][0]['conversation']['peer']
    text4 = messages['items'][0]['conversation']['last_message_id']
    text5 = messages['items'][0]['conversation']['peer']['id']
    text6 = messages['items'][0]['conversation']['peer']["type"]
    text7 = messages["items"][0]["last_message"]

    text80 = messages["items"][0]["last_message"]["date"]
    time_bc = datetime.datetime.fromtimestamp(int(text80))
    text8 = str(time_bc.strftime('%d.%m.%Y-%H.%M.%S'))

    text9 = messages["items"][0]["last_message"]["from_id"]  # id пользователя от которого пришло сообщение
    text10 = messages["items"][0]["last_message"]["text"]

    # print(f'text1 = messages["items"][0]- \n {text1} \n')
    # print(f'text2 = messages["items"][0]["conversation"]- \n {text2} \n')
    # print(f'text3 = messages["items"][0]["conversation"]["peer"]- \n {text3} \n')
    # print(f'text4 = messages["items"][0]["conversation"]["last_message_id"]- \n {text4} \n')
    # print(f'text5 = messages["items"][0]["conversation"]["peer"]["id"]- \n {text5} \n')
    # print(f'text6 = messages["items"][0]["conversation"]["peer"]["type"]- \n {text6} \n')
    # print(f'text7 = messages["items"][0]["last_message"]- \n {text7} \n')

    # print(f'text8 = messages["items"][0]["last_message"]["date"]- \n {text80} -> {text8} \n')

    # print(f'text9 = messages["items"][0]["last_message"]["from_id"]- \n {text9} \n')
    # print(f'text10 = messages["items"][0]["last_message"]["text"]- \n {text10} \n')

    user_id = messages['items'][0]['last_message']['from_id']
    # print(user_id)
    print(f'{text8} Ползователь: {user_id}, сообщил: {text10}')
    return user_id


# get_last_msg()


# send_message = vk_session.method("messages.send", {"user_id": 158189236, "messages": "What up? Repeat again!", "random_id": random.randint(1, 1000)})
# print(send_message)

def get_user_status(user_id):
    status = vk_session.method("status.get", {"user_id": user_id})
    print(status["text"])

def get_group_status(group_id):
    status = vk_session.method("status.get", {"group_id": group_id})
    print(status["text"])


def set_user_status():
    vk.status.set(text="My studying Python in progress!")


def set_group_status():
    vk.status.set(text="Service under development!", group_id=218321292)


set_user_status()
set_group_status()

get_user_status(158189236)
get_group_status(218321292)
