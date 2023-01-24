import os
from vk_api.longpoll import VkLongPoll, VkEventType
import random
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
vk_longpoll = VkLongPoll(group_vk_session)  # Создаем другую переменную (vk_longpoll), где переменную сесии (group_vk_session) подключаем к классу VkLongPoll.
# vk_session._auth_token()  # Авторизация токена.


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


def get_user_status(user_id):
    status = vk_session.method("status.get", {"user_id": user_id})
    print(status["text"])


# def get_group_status(group_id):
#     status = vk_session.method("status.get", {"group_id": group_id})
#     print(status["text"])

def get_group_status(group_id):
    status = vk.status.get(group_id=group_id)
    print(status["text"])


def set_user_status(text):
    vk.status.set(text=text)


# def set_group_status():
#     vk.status.set(text="Service bot under development!", group_id=218321292)

def set_group_status(text, group_id):
    vk_session.method("status.set", {"text": text, "group_id": group_id})


def get_friends_status(user_id):
    friends = vk_session.method("friends.get", {"user_id": user_id})
    num = 0
    for friend in friends["items"]:
        friend_info = vk.users.get(user_ids=friend)
        # print(f'{num}. {friend_info}')
        try:
            num += 1
            friend_status = vk.status.get(user_id=friend)
            if friend_status["text"] == "":
                continue
            else:
                print(
                    f'{num}. {friend_info[0]["first_name"]} {friend_info[0]["last_name"]} <-> {friend_status["text"]}')
        except vk_api.exceptions.ApiError:
            num -= 1
            pass


def get_friends_is_banned(user_id):
    friends = vk_session.method("friends.get", {"user_id": user_id})
    num_bunned = 0
    for friend in friends["items"]:
        friend_info = vk.users.get(user_ids=friend)
        # print(f'{num}. {friend_info}')
        try:
            num_bunned += 1
            print(
                f'{num_bunned}. {friend_info[0]["first_name"]} {friend_info[0]["last_name"]} <-> {friend_info[0]["deactivated"]}')
        except KeyError:
            num_bunned -= 1
            pass

def get_friend_info(user_id):
    friends = vk_session.method("friends.get", {"user_id": user_id})
    num = 0
    for friend in friends["items"]:
        friend_info = vk.users.get(user_ids=friend)
        # print(f'{num}. {friend_info}')
        try:
            num += 1
            friend_status = vk.status.get(user_id=friend)
            print(f'{num}. {friend_info[0]["id"]}: {friend_info[0]["first_name"]} {friend_info[0]["last_name"]} <-> {friend_status["text"]}')
        except vk_api.exceptions.ApiError:
            num -= 1
            pass

def get_random_id():
    return random.getrandbits(31) * random.choice([-1, 1])


# def send_message(user_id, message):
#     vk_session.method("messages.send", {
#         "user_id": user_id,
#         "message": message,
#         "random_id": randrange(10 ** 7),
#     })


def bot_send_msg(user_id, message):
    group_vk_session.method("messages.send", {
        "user_id": user_id,
        "message": message,
        "random_id": randrange(10 ** 7),
    })

for event in vk_longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        text = event.text.lower()
        user_id = event.user_id

        if text == "hi":
            bot_send_msg(user_id, " 3 Привет! What's up?:)")


# get_last_msg()

# set_user_status("My studying Python in progress! Like, Like)")
# set_group_status("Now service bot under development!", 218321292)

# get_user_status(158189236)
# get_group_status(218321292)

# get_friends_status(158189236)
# get_friends_is_banned(158189236)

# get_friend_info(158189236)

# send_message(158189236)
# send_message(205642650)
# send_message(22221403, "звони на МТС мой 2й номер: ")
# send_message(22221403, "")
# send_message(22221403, "у меня 'Волна' если че")
