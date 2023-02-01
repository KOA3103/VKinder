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
vk_group_got_api = group_vk_session.get_api()  # Создаем другую переменную (vk), где переменную сесии (vk_session) подключаем к api списку методов.
vk_longpoll = VkLongPoll(
    group_vk_session)  # Создаем другую переменную (vk_longpoll), где переменную сесии (group_vk_session) подключаем к классу VkLongPoll.


def send_msg(user_id, message):
    """МЕТОД ДЛЯ ОТПРАВКИ СООБЩЕНИЙ"""
    vk_group_got_api.messages.send(
        user_id=user_id,
        message=message,
        random_id=randrange(10 ** 7)
    )


def name(user_id):
    """ПОЛУЧЕНИЕ ИМЕНИ ПОЛЬЗОВАТЕЛЯ, КОТОРЫЙ НАПИСАЛ БОТУ"""
    user_info = vk_group_got_api.users.get(user_id=user_id)
    # print(user_info)
    name = user_info[0]['first_name']
    print(name)
    return name



for event in vk_longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        request = event.text.lower()
        user_id = event.user_id
        name_user = name(user_id)
        if request == "hi":
            send_msg(user_id, f"Хай, {name_user}")
        elif request == "bye":
            send_msg(user_id, f"Пока(( {name_user}")
        else:
            send_msg(user_id, f"{name_user}. Бот не понял! Повтори.")



def users_search(city):  # group_token is unavailable for this metod users.search.
    res = vk_group_got_api.users.search(
        sort=0,
        hometown=city,
        sex=1,  # 1— женщина, 2 — мужчина, 0 — любой (по умолчанию).
        status=1,  # 1 — не женат или не замужем, 6 — в активном поиске.
        age_from=16,
        age_to=50,
        has_photo=1,  # 1 — искать только пользователей с фотографией, 0 — искать по всем пользователям
        count=1000
    )
    print(res)
    # print(res['items'])
    # print(res['items'][0]["id"])
    number = 0
    # print(res['items'][0]['first_name'], res['items'][0]['last_name'])
    for user in res['items']:
        number += 1
        print(f'{number}. {user["first_name"]} {user["last_name"]}, {user["id"]} ')
    print(res['count'])


# users_search("москва")
users_search("Бахчисарай")

def user_photo(owner_id):
    res = vk.photos.get(
        owner_id=str(owner_id),
        album_id="wall",  # wall — фотографии со стены, profile — фотографии профиля.
        extended=1  # 1 — будут возвращены дополнительные поля likes, comments, tags, can_comment, reposts. По
        # умолчанию: 0.
    )
    number = 0
    for user in res['items']:
        number += 1
        print(1, user["sizes"])
        for size in user["sizes"]:
            print(number)


            if size["type"] == "w":
                print(number, "w", size["url"])
                if size["type"] == "r":
                    print(number, "r", size["url"])
                    if size["type"] == "q":
                        print(number, "q", size["url"])
                        if size["type"] == "z":
                            print(number, "z", size["url"])
                            if size["type"] == "y":
                                print(number, "y", size["url"])
                                if size["type"] == "x":
                                    print(number, "x", size["url"])
        # if user["sizes"][0] == "w":

        # print(f'{number}.1 m {user["sizes"][0]}')
        # print(f'{number}.2 o {user["sizes"][1]}')
        # print(f'{number}.3 p {user["sizes"][2]}')
        # print(f'{number}.4 q {user["sizes"][3]}')
        # print(f'{number}.5 r {user["sizes"][4]}')
        # print(f'{number}.6 s {user["sizes"][5]}')
        # print(f'{number}.7 w {user["sizes"][6]}')
        # try:
        #     print(f'{number}.8 x {user["sizes"][7]}')
        # except IndexError:
        #     continue
        # try:
        #     print(f'{number}.9 y {user["sizes"][8]}')
        # except IndexError:
        #     continue
        # try:
        #     print(f'{number}.10 z {user["sizes"][9]}')
        # except IndexError:
        #     continue

        # if user["sizes"][6]["type"] == "w":
        #     print(user["sizes"][6]["url"])


        # print(user)
    # pprint(res)

user_photo("52968274")