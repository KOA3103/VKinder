from vk_api.longpoll import VkEventType, VkLongPoll
from bot import *
from db import *
from config import *


for event in bot.longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        request = event.text.lower()
        user_id = event.user_id
        if request == 'поиск' or request == 'f':
            bot.get_age_of_user(user_id)
            bot.get_target_city(user_id)
            bot.looking_for_persons(user_id)  # выводит список в чат найденных людей и добавляет их в базу данных.
            bot.show_found_person(user_id)  # выводит в чат инфо одного человека из базы данных.
        elif request == 'удалить' or request == 'd':
            creating_database()  # удаляет существующую БД и создает новую.
            bot.send_msg(user_id, f'  Сейчас наберите "Поиск" ')
        elif request == 'смотреть' or request == 's':
            bot.show_found_person(user_id)
        else:
            bot.send_msg(user_id, f'{bot.name(user_id)} Бот готов к поиску, наберите: \n '
                                      f' "Поиск или f" - Поиск людей. \n'
                                      f' "Удалить или d" - удаляет старую БД и создает новую. \n'
                                      f' "Смотреть или s" - просмотр следующей записи в БД.')

