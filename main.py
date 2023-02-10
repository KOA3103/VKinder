from vk_api.longpoll import VkEventType, VkLongPoll
from bot import *
from db import *
from config import *

for event in bot.longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        request = event.text.lower()
        user_id = event.user_id

        if request == 'новый поиск':
            creating_database()  # удаляет существующую БД и создает новую.
            bot.send_msg(user_id, f'{bot.name(user_id)}. Бот в процессе поиска')
            bot.send_msg(user_id, f'{bot.get_age_of_user(user_id)}{bot.get_target_city(user_id)}')
            bot.looking_for_persons(user_id)  # выводит список в чат найденных людей и добавляет их в базу данных.
            bot.show_found_person(user_id)  # выводит в чат инфо одного человека из базы данных.
        elif request == 'искать дальше':
            bot.send_msg(user_id, f' {bot.get_age_of_user(user_id)}{bot.get_target_city(user_id)}')
            bot.looking_for_persons(user_id)
            bot.show_found_person(user_id)
        elif request == 'смотреть':

            for i in range(0, 1000):
                offset += 1
                bot.show_found_person(user_id)
                break

        else:
            bot.send_msg(user_id, f'{bot.name(user_id)} Бот готов к поиску, наберите: \n '
                                  f' "Новый поиск" - найденных людей помещаем в БД. \n'
                                  f' "Искать дальше" - новых найденных добавляет к уже созданной БД. \n'
                                  f' "Смотреть" - просмотр следующей записи в БД.')
