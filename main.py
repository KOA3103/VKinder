import os
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from random import randrange
import datetime
import vk_api
import time
import json
from pprint import pprint
from config import user_token, group_token


vk_session = vk_api.VkApi(token=user_token, api_version='5.131')  # Создаем переменную сесии.
vk = vk_session.get_api()  # Создаем другую переменную (vk), где переменную сесии (vk_session) подключаем к api списку методов.
vk_session._auth_token()  # Авторизация токена.

group_vk_session = vk_api.VkApi(token=group_token, api_version='5.131')  # Создаем переменную сесии group_token.
vk_group_get_api = group_vk_session.get_api()  # Создаем другую переменную (vk), где переменную сесии (vk_session) подключаем к api списку методов.
vk_longpoll = VkLongPoll(
    group_vk_session)  # Создаем другую переменную (vk_longpoll), где переменную сесии (group_vk_session) подключаем к классу VkLongPoll.


def send_msg(user_id, message):
    # group_vk_session.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7)}) # идентичный коду ниже
    vk_group_get_api.messages.send(
        user_id=user_id,
        message=message,
        random_id=randrange(10 ** 7)
    )

def get_user_info(user_id):
    # user_info = group_vk_session.method('users.get', {'user_id': user_id}) # идентичный коду ниже
    user_info = vk_group_get_api.users.get(user_id=user_id)
    # print(user_info)
    name = user_info[0]['first_name']
    return name


for event in vk_longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        request = event.text.lower()
        name = get_user_info(event.user_id)
        user_id = event.user_id
        if request == "hi":
            send_msg(user_id, f"Хай, {name}")
        elif request == "bye":
            send_msg(user_id, f"Пока(( {name}")
        else:
            send_msg(user_id, f"{name}. Бот не понял! Повтори.")




