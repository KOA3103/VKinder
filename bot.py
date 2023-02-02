from vk_api.longpoll import VkLongPoll, VkEventType
from random import randrange
import vk_api
from config import user_token, group_token


class Bot:
    def __init__(self):
        print('Bot was created')
        self.vk_user = vk_api.VkApi(token=user_token)  # Создаем переменную сесии, авторизованную личным токеном пользователя.
        self.vk_user_got_api = self.vk_user.get_api()  # # переменную сессии vk_user подключаем к api списку методов.
        self.vk_user._auth_token()  # Авторизация токена.
        self.vk_group = vk_api.VkApi(token=group_token)  # Создаем переменную сесии, авторизованную токеном сообщества.
        self.vk_group_got_api = self.vk_group.get_api()  # переменную сессии vk_group подключаем к api списку методов.
        self.longpoll = VkLongPoll(self.vk_group)  # переменную сессии vk_group_got_api подключаем к Long Poll API, позволяет работать с событиями из вашего сообщества в реальном времени.


    def send_msg(self, user_id, message):
        """METHOD FOR SENDING MESSAGES"""
        self.vk_group_got_api.messages.send(
            user_id=user_id,
            message=message,
            random_id=randrange(10 ** 7)
        )

    def name(self, user_id):
        """GETTING THE NAME OF THE USER WHO WRITTEN TO THE BOT"""
        user_info = self.vk_group_got_api.users.get(user_id=user_id)
        # print(user_info)
        name = user_info[0]['first_name']
        return name

    def get_user_info(self, user_id):
        info = self.vk_user_got_api.users.get(user_id=user_id)
        print(info[0]['first_name'])

    # get_user_info(22403)

    def looking_for_gender(self, user_id):
        """LOOKING FOR THE OPPOSITE GENDER TO THE USER"""
        info = self.vk_user_got_api.users.get(
            user_id=user_id,
            fields="sex"
        )
        if info[0]['sex'] == 1:  # 1 — женщина, 2 — мужчина,
            return f'2 - ищем мужчину'

        else:
            return f'1 - ищем женщину'

    # print(looking_for_gender(52968274))


    def users_search(self, city):  # group_token is unavailable for this metod users.search.
        """ SEARCH FOR A PERSON BASED ON THE DATA RECEIVED """
        res = self.vk_user_got_api.users.search(
            sort=0,
            hometown="Бахчисарай",
            sex=1,  # 1— женщина, 2 — мужчина, 0 — любой (по умолчанию).
            status=1,  # 1 — не женат или не замужем, 6 — в активном поиске.
            age_from=16,
            age_to=25,
            has_photo=1,  # 1 — искать только пользователей с фотографией, 0 — искать по всем пользователям
            count=100
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

    def user_photo(self, owner_id):
        """GETTING USER PHOTOS"""
        res = self.vk_user_got_api.photos.get(
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


bot = Bot()