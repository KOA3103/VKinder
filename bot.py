from vk_api.longpoll import VkLongPoll, VkEventType
import datetime
import vk_api
from config import user_token, group_token
from random import randrange
from pprint import pprint
from db import *
import psycopg2
from psycopg2 import errors

offset = 0


class Bot:
    def __init__(self):
        print('Bot was created')
        self.vk_user = vk_api.VkApi(
            token=user_token)  # Создаем переменную сессии, авторизованную личным токеном пользователя.
        self.vk_user_got_api = self.vk_user.get_api()  # # переменную сессии vk_user подключаем к api списку методов.
        self.vk_user._auth_token()  # Авторизация токена.
        self.vk_group = vk_api.VkApi(token=group_token)  # Создаем переменную сесии, авторизованную токеном сообщества.
        self.vk_group_got_api = self.vk_group.get_api()  # переменную сессии vk_group подключаем к api списку методов.
        self.longpoll = VkLongPoll(
            self.vk_group)  # переменную сессии vk_group_got_api подключаем к Long Poll API,
        # позволяет работать с событиями из вашего сообщества в реальном времени.

    def send_msg(self, user_id, message):
        """method for sending messages"""
        self.vk_group_got_api.messages.send(
            user_id=user_id,
            message=message,
            random_id=randrange(10 ** 7)
        )

    def name(self, user_id):
        """getting the name of the user who written to the bot"""
        user_info = self.vk_group_got_api.users.get(user_id=user_id)
        # print(user_info)
        name = user_info[0]['first_name']
        return name

    def get_user_info(self, user_id):
        info = self.vk_user_got_api.users.get(
            user_id=user_id,
            fields="counters, "  # Количество различных объектов у пользователя.
                   "city, "
                   "bdate",
        )
        # print(info[0]['first_name'])
        # print(info[0]['city'])
        print(info[0]['bdate'])

    def naming_of_years(self, years, till=None):
        """addition to years"""
        if till is True:
            name_years = [1, 21, 31, 41, 51, 61, 71, 81, 91, 101]
            if years in name_years:
                return f'{years} года'
            else:
                return f'{years} лет'
        else:
            name_years = [2, 3, 4, 22, 23, 24, 32, 33, 34, 42, 43, 44, 52, 53, 54, 62, 63, 64]
            if years == 1 or years == 21 or years == 31 or years == 41 or years == 51 or years == 61:
                return f'{years} год'
            elif years in name_years:
                return f'{years} года'
            else:
                return f'{years} лет'

    def get_years_of_person(self, bdate: str) -> object:
        """determining the number of years"""
        bdate_splited = bdate.split(".")
        month = ""
        try:
            reverse_bdate = datetime.date(int(bdate_splited[2]), int(bdate_splited[1]), int(bdate_splited[0]))
            today = datetime.date.today()
            years = (today.year - reverse_bdate.year)
            if reverse_bdate.month >= today.month and reverse_bdate.day > today.day or reverse_bdate.month > today.month:
                years -= 1
            name_years = [2, 3, 4, 22, 23, 24, 32, 33, 34, 42, 43, 44, 52, 53, 54, 62, 63, 64]
            if years == 1 or years == 21 or years == 31 or years == 41 or years == 51 or years == 61:
                return f'{years} год'
            elif years in name_years:
                return f'{years} года'
            else:
                return f'{years} лет'
        except IndexError:
            if bdate_splited[1] == "1":
                month = "января"
            elif bdate_splited[1] == "2":
                month = "февраля"
            elif bdate_splited[1] == "3":
                month = "марта"
            elif bdate_splited[1] == "4":
                month = "апреля"
            elif bdate_splited[1] == "5":
                month = "мая"
            elif bdate_splited[1] == "6":
                month = "июня"
            elif bdate_splited[1] == "7":
                month = "июля"
            elif bdate_splited[1] == "8":
                month = "августа"
            elif bdate_splited[1] == "9":
                month = "сентября"
            elif bdate_splited[1] == "10":
                month = "октября"
            elif bdate_splited[1] == "11":
                month = "ноября"
            elif bdate_splited[1] == "12":
                month = "декабря"
            return f'День рождения {int(bdate_splited[0])} {month}.'

    def get_age_of_user(self, user_id):
        """determine the user's age"""
        global age_from, age_to
        try:
            info = self.vk_user_got_api.users.get(
                user_ids=user_id,
                fields="bdate",
            )[0]['bdate']
            num_age = self.get_years_of_person(info).split()[0]
            age_from = num_age
            age_to = num_age
            if num_age == "День":
                print(f'Ваш {self.get_years_of_person(info)}')
                self.send_msg(user_id,
                              f'   Бот ищет людей вашего возраста, но в ваших настройках профиля установлен пункт "Показывать только месяц и день рождения"! \n'
                              f'   Поэтому, введите возраст поиска, на пример от 21 года и до 35 лет, в формате : 21-35 (или 21 конкретный возраст 21 год).'
                              )
                for event in self.longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                        age = event.text
                        a = age.rsplit("-")
                        age_from = int(a[0])
                        age_to = int(a[1])
                        if age_from == age_from:
                            return f' Ищем возраст {self.naming_of_years(age_to, True)}, '
                        return f' Ищем возраст в пределах от {age_from} и до {self.naming_of_years(age_to, True)}, '

            return f' Ищем вашего возраста {self.naming_of_years(age_to)}, '
        except KeyError:
            print(f'День рождения скрыт настройками приватности!')
            self.send_msg(user_id,
                          f' Бот ищет людей вашего возраста, но в ваших в настройках профиля установлен пункт "Не показывать дату рождения". '
                          f'\n Поэтому, введите возраст поиска, на пример от 21 года и до 35 лет, в формате : 21-35 (или 21 конкретный возраст 21 год).'
                          )
            for event in self.longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    age = event.text
                    try:
                        a = age.rsplit("-")
                        age_from = int(a[0])
                        age_to = int(a[1])
                        if age_from == age_to:
                            return f' Ищем возраст {self.naming_of_years(age_to, True)}, '
                        return f' Ищем возраст в пределах от {age_from} и до {self.naming_of_years(age_to, True)}, '
                    except IndexError:
                        age_from = age
                        age_to = age
                        return f' Ищем возраст {self.naming_of_years(age_to, True)}, '
                    except NameError:
                        return f' Введен не правильный числовой формат!  '

    def get_target_city(self, user_id):
        """define city to search"""
        global city_id, city_title
        self.send_msg(user_id,
                      f' Введите "Да" - поиск будет произведен в городе указанный в профиле.'
                      f' Или введите название города, например: Москва'
                      )
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                answer = event.text.lower()
                if answer == "да" or answer == "yes":
                    info = self.vk_user_got_api.users.get(
                        user_id=user_id,
                        fields="city"
                    )
                    city_id = info[0]['city']["id"]
                    city_title = info[0]['city']["title"]
                    return f' в городе {city_title}.'
                else:
                    cities = self.vk_user_got_api.database.getCities(
                        country_id=1,
                        q=answer.capitalize(),
                        need_all=1,
                        count=1000
                    )['items']
                    for i in cities:
                        if i["title"] == answer.capitalize():
                            city_id = i["id"]
                            # print(11, city_id)
                            city_title = answer.capitalize()
                            # print(111, city_title)
                            return f' в городе {city_title}'

    def looking_for_gender(self, user_id):
        """looking for the opposite gender to the user"""
        info = self.vk_user_got_api.users.get(
            user_id=user_id,
            fields="sex"
        )
        if info[0]['sex'] == 1:  # 1 — женщина, 2 — мужчина,
            print(f'Ваш пол женский, ищем мужчину.')
            return 2
        elif info[0]['sex'] == 2:
            print(f'Ваш пол мужской, ищем женщину.')
            return 1
        else:
            print("ERROR!!!")

    def looking_for_persons(self, user_id):
        """ search for a person based on the data received """
        res = self.vk_user_got_api.users.search(  # group_token is unavailable for this method users.search.
            sort=0,  # 1 — по дате регистрации, 0 — по популярности.
            city=city_id,
            hometown=city_title,
            sex=self.looking_for_gender(user_id),  # 1— женщина, 2 — мужчина, 0 — любой (по умолчанию).
            status=1,  # 1 — не женат или не замужем, 6 — в активном поиске.
            age_from=age_from,
            age_to=age_to,
            has_photo=1,  # 1 — искать только пользователей с фотографией, 0 — искать по всем пользователям
            count=1000,
            fields="about, "  # Содержимое поля «О себе» из профиля.
                   "activities, "  # Содержимое поля «Деятельность» из профиля.
                   "bdate, "  # Дата рождения. Возвращается в формате D.M.YYYY или D.M (если год рождения скрыт). Если дата рождения скрыта целиком, поле отсутствует в ответе.
                   "status, "
                   "can_write_private_message, "  # Информация о том, может ли текущий пользователь отправить личное сообщение. Возможные значения: 1 — может; 0 — не может.
                   "city, "  # Информация о городе, указанном на странице пользователя в разделе «Контакты».
                   "common_count, "  # Количество общих друзей с текущим пользователем.
                   "contacts, "  # Информация о телефонных номерах пользователя. Если данные указаны и не скрыты настройками приватности.
                   "domain, "  # Короткий адрес страницы.
                   "home_town, "  # Название родного города.
                   "interests, "  # Содержимое поля «Интересы» из профиля.
                   "movies, "  # Содержимое поля «Любимые фильмы» из профиля пользователя.
                   "music, "  # Содержимое поля «Любимая музыка» из профиля пользователя.
                   "occupation, "  # Информация о текущем роде занятия пользователя.
        )
        # pprint(res)
        # print(res['items'])
        # print(res['items'][0]["id"])
        number = 0
        for person in res["items"]:
            if not person["is_closed"]:
                first_name = person["first_name"]
                last_name = person["last_name"]
                # age = self.get_years_of_person(person["bdate"])
                id_vk = person["id"]
                vk_link = 'vk.com/' + person["domain"]
                request_from = user_id
                if "city" in person and person["city"]["id"] == city_id and person["city"]["title"] == city_title:
                    city = f'Город {person["city"]["title"]}'
                    try:
                        number += 1
                        insert_found_person(first_name, last_name, id_vk, vk_link, request_from)
                        # self.send_msg(user_id, f'{number}. {first_name} {last_name}, {age}, {city}, {vk_link}')
                    except psycopg2.errors.UniqueViolation:
                        pass
                else:
                    try:
                        city = f'Город {person["home_town"]}'
                        try:
                            number += 1
                            insert_found_person(first_name, last_name, id_vk, vk_link, request_from)  # вставка в БД.
                            # self.send_msg(user_id, f'{number}. {first_name} {last_name}, {age}, {city}, {vk_link}')
                        except psycopg2.errors.UniqueViolation:
                            pass
                    except KeyError:
                        pass
        print(f'Bot found {number} opened profiles for viewing from {res["count"]}')
        return f'Бот нашел {number} открытых профилей для просмотра из {res["count"]}'

    def photo_of_found_person(self, user_id):
        """getting a photo of a found person"""
        global attachments
        res = self.vk_user_got_api.photos.get(
            owner_id=user_id,
            album_id="profile",  # wall — фотографии со стены, profile — фотографии профиля.
            extended=1,  # 1 — будут возвращены дополнительные поля likes, comments, tags, can_comment, reposts. По
            # умолчанию: 0.
            count=30
        )
        print(res)
        dict_photos = dict()
        for i in res['items']:
            photo_id = str(i["id"])
            i_likes = i["likes"]
            # i_comments = i["comments"]
            if i_likes["count"]:
                likes = i_likes["count"]
                dict_photos[likes] = photo_id
        list_of_ids = sorted(dict_photos.items(), reverse=True)
        attachments = []
        photo_ids = []
        for i in list_of_ids:
            photo_ids.append(i[1])
        try:
            attachments.append('photo{}_{}'.format(user_id, photo_ids[0]))
            attachments.append('photo{}_{}'.format(user_id, photo_ids[1]))
            attachments.append('photo{}_{}'.format(user_id, photo_ids[2]))
            # print(attachments)
            return attachments
        except IndexError:
            attachments.append('photo{}_{}'.format(user_id, photo_ids[0]))
            # print(attachments)
            return attachments

    def found_person_info(self, show_person_id):
        """information about the found person"""
        res = self.vk_user_got_api.users.get(
            user_ids=show_person_id,
            fields="about, "  # Содержимое поля «О себе» из профиля.
                   "activities, "  # Содержимое поля «Деятельность» из профиля.
                   "bdate, "  # Дата рождения. Возвращается в формате D.M.YYYY или D.M (если год рождения скрыт). Если дата рождения скрыта целиком, поле отсутствует в ответе.
                   "status, "
                   "can_write_private_message, "  # Информация о том, может ли текущий пользователь отправить личное сообщение. Возможные значения: 1 — может; 0 — не может.
                   "city, "  # Информация о городе, указанном на странице пользователя в разделе «Контакты».
                   "common_count, "  # Количество общих друзей с текущим пользователем.
                   "contacts, "  # Информация о телефонных номерах пользователя. Если данные указаны и не скрыты настройками приватности.
                   "domain, "  # Короткий адрес страницы.
                   "home_town, "  # Название родного города.
                   "interests, "  # Содержимое поля «Интересы» из профиля.
                   "movies, "  # Содержимое поля «Любимые фильмы» из профиля пользователя.
                   "music, "  # Содержимое поля «Любимая музыка» из профиля пользователя.
                   "occupation"  # Информация о текущем роде занятия пользователя.
        )
        first_name = res[0]["first_name"]
        last_name = res[0]["last_name"]
        age = self.get_years_of_person(res[0]["bdate"])
        vk_link = 'vk.com/' + res[0]["domain"]
        try:
            city = f'Город {res[0]["city"]["title"]}'
        except KeyError:
            city = f'Город {res[0]["home_town"]}'
        print(f'{first_name} {last_name}, {age}, {city}. {vk_link}')
        return f'{first_name} {last_name}, {age}, {city}. {vk_link}'

    def send_photo(self, user_id, message, attachments):
        """method for sending photos"""
        self.vk_group_got_api.messages.send(
            user_id=user_id,
            message=message,
            random_id=randrange(10 ** 7),
            attachment=",".join(attachments)
        )

    def show_found_person(self, user_id):
        """show person from database"""
        print(f'Поиск от пользователя: {user_id}')
        try:
            self.send_msg(user_id, self.found_person_info(select(offset)[2]))
            self.send_photo(user_id, 'Три фото с максимальными лайками', self.photo_of_found_person(select(offset)[2]))
            insert_data_seen_person(select(offset)[2], offset)  # offset ( select(offset)[2] = fp.id_vk )
        except TypeError:
            return f' Похоже просмотренны все профили из БД. \n' \
                   f' Наберите "Искать дальше" для поиска и добавления в БД.'


bot = Bot()
