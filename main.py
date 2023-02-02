from bot import *

for event in Bot().longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        request = event.text.lower()
        user_id = event.user_id
        if request == 'начать поиск':
            bot.users_search(user_id)
            bot.send_msg(user_id, f'{bot.name(user_id)}. Бот найдет для тебя пару, жми на кнопку "Начать поиск"')
            bot.send_msg(user_id, f'{bot.looking_for_gender(user_id)}')
        elif request == 'вперёд':
            print("ура вперед!")
        else:
            bot.send_msg(user_id, f'{bot.name(user_id)}. Нажми на кнопку "Смотреть дальше" или кнопку "Начать новый поиск"')
