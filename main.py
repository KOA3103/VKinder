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
            delete_table_seen_person()  # удаляет существующую БД.
            create_table_seen_person()  # создает новую БД.
            bot.send_msg(user_id, f' База данных отчищена! Сейчас наберите "Поиск" или F ')
        elif request == 'смотреть' or request == 's':
            if bot.get_found_person_id() != 0:
                bot.show_found_person(user_id)
            else:
                bot.send_msg(user_id, f' В начале наберите Поиск или f.  ')
        else:
            bot.send_msg(user_id, f'{bot.name(user_id)} Бот готов к поиску, наберите: \n '
                                      f' "Поиск или F" - Поиск людей. \n'
                                      f' "Удалить или D" - удаляет старую БД и создает новую. \n'
                                      f' "Смотреть или S" - просмотр следующей записи в БД.')

