import requests
from datetime import date
from random import randrange
from DB_vkinder import insert_user, insert_find, select_elect



class VkDownloader():

    def __init__(self, token):
        self.token = token


    def user_info(self, user_id):
        url_info = 'https://api.vk.com/method/users.get'
        params = {
            'user_ids': user_id,
            'fields': 'sex, city, maiden_name, bdate',
            'access_token': self.token,
            'v': 5.131
        }
        res = requests.get(url_info, params=params).json()
        for value in res["response"]:
            city = value['city']#ваш город
            sex = value['sex']#ваш пол
            bdate = value['bdate']#ваша дата рождения
            name = value['first_name'] + ' ' + value['last_name']#ваше имя и фамилия
            user_list = [city, sex, name, bdate, user_id]#общий лист с вашими данными
            insert_user(user_list)
            return user_list

    # Используется только Токен персональный
    def user_search(self, data):
        url_info = 'https://api.vk.com/method/users.search'
        if data[1] == 1:#условие по полу
            sex = 2
        else:
            sex = 1
        #калькулятор по вычислению лет
        today = date.today()
        get_year = data[3].split('.')
        day = int(get_year[0])
        month = int(get_year[1])
        year = int(get_year[2])
        age = today.year - year - ((today.month, today.day) < (month, day))
        params = {
            'count': 1000,#макс выгрузка 1000 значений
            'fields': 'photo_max, has_photo, is_closed',#доп передаваемые поля
            'city': data[0]["id"],#город
            'sex': sex,#пол
            'age_from': age - 3,#разброс -
            'age_to': age + 3,#разброс +
            'access_token': self.token,
            'v': 5.131
            }
        res = requests.get(url_info, params=params).json()

        return res#возврат json пользователей
        

    def get_photo(self, id):#функция выгрузки фото с профиля
        photo_all = []#список для всех фото одного пользователя
        photo_3 = []#список для 3 фото
        num = []#список для отбора по лайкам
        url_photo = 'https://api.vk.com/method/photos.getProfile'
        params = {
            'owner_id': id,
            'album_id': 'profile',
            'extended': 1,
            'photo_sizes': 1,
            'access_token': self.token,
            'v': 5.131
        }
        res = requests.get(url_photo, params=params).json()

        #находим ссылки на фото и количество лайков, создаем словари и добавляем их в списко
        for values in res["response"]["items"]:
            file_likes = values["likes"]["count"]#количество лайков фото
            id_photo = values["id"]#id фото
            file_photo = {'id_photo': id_photo, 'likes': file_likes}#отдельный словарик для фото+лайк
            photo_all.append(file_photo)

        #все лайки переношу в список, сортирую, остается 3 самых больших значения
        for links in photo_all:
            num.append(links['likes'])#собираем лайки фоток в один список
        n = min(3, len(num))#проверяем на количество в листе лайков и формируем от 1 до 3 в зависимости от количества в профиле
        max_numbers = sorted(num, reverse=True)[:n]#сортируем
        for links in photo_all:
            if links['likes'] in max_numbers and len(photo_3) < 3:
                photo_3.append(links['id_photo'])#находим фото по лайкам
        return photo_3

    def get_profile_1(self, user_id):#функция для вызова всех функций
        user_list = self.user_info(user_id)#получаем данные нашего пользователя
        get_info_max_id = self.user_search(user_list)#производим поиск подходящих пользователей
        profile_needs = []#пустой список для отобранных пользователей по критериям
        #ДЕЛАЕМ ОТБОР ПО ОТКРЫТОМУ ПРОФИЛЮ И ИМЕЮЩЕЙСЯ ФОТКЕ
        for values in get_info_max_id["response"]["items"]:
            if values["is_closed"] == False and values["has_photo"] == 1:#сортируем по открытому акку и наличию фото
                profile_needs.append(values)#добавляем в лист
        #РАНДОМ ДЛЯ profile_needs
        profile_info = self.extract_random(profile_needs)
        #ВЫДЕЛЯЕМ ЭЛЕМЕНТЫ ЕДИНИЧНОГО id
        id_person = profile_info["id"]
        #ПОЛУЧАЕМ ЗНАЧЕНИЕ ДЛЯ 3 ФОТО ПО id
        photo_profile = self.get_photo(id_person)#получаем инфу 3 фоток
        attachment = []#создаем пустой список для поля attachment
        for photo in photo_profile:#формирование attachment для функции message_send_photo на печать фото
            attachment_one = f'photo{id_person}_{photo}'#формируем для одного фото
            attachment.append(attachment_one)#добавляем в список
        attachment = ','.join(attachment)#соединяем для вывода сразу всех значений в функции message_send_photo
        link_id = f'https://vk.com/id{id_person}'#Получение ссылки на профиль
        name = profile_info["first_name"] + ' ' + profile_info["last_name"]#формирование имя и фамилии
        profile = {'id': id_person, 'name': name, 'link_id': link_id, 'attachment': attachment, 'user_id': user_list[4]}
        profile_list = []
        profile_list.append(profile)
        return profile_list#Возвращаем инфу о профиле для вывода в функцию message_send_photo

    def extract_random(self, lst):#функция рандома с удалением индекса из списка
        if not lst:
            return None
        index = randrange(len(lst))
        return lst.pop(index)
    
    
    def message_send_photo(self, user_id, bottoken, num, profile_list=[]):#функция принимает токен группы и словарь с данными людей
        if num == 1:
            profile_list = self.get_profile_1(user_id)#получаем профиль искомого пользователя
            insert_find(profile_list)
        else:
            profile_list = select_elect(user_id)#получаем список избранных для печати
        for profile_1 in profile_list:
            user_id = profile_1['user_id']#ваш id
            name = profile_1['name']#имя и фамилия пользователя
            link = profile_1['link_id']#ссылка на профиль пользователя
            message = f'{name}\n {link}'#сообщение для ответа
            att = profile_1['attachment']#а вот и наш attachment, который присылает фото в сообщении
            url_photo = 'https://api.vk.com/method/messages.send'
            params = {
                'user_id': user_id,
                'random_id': randrange(10 ** 7),
                'message': message,# имя, фамилия и ссылка на профиль
                'attachment': att,#для вывода 3 фоток сразу
                'access_token': bottoken,
                'v': 5.131
            }

            requests.get(url_photo, params=params)#печатаем в чат


        return profile_list
