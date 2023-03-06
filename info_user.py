import requests
from datetime import date
from random import randrange
from DB_vkinder import insert_user
from config_read import perstoken, bottoken


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
            city = value['city']
            sex = value['sex']
            bdate = value['bdate']
            name = value['first_name'] + ' ' + value['last_name']
            user_list = [city, sex, name, bdate, user_id]

            # insert_user(user_list)
            return user_list

    # Используется только Токен персональный
    def user_search(self, data):
        url_info = 'https://api.vk.com/method/users.search'
        if data[1] == 1:
            sex = 2
        else:
            sex = 1
        today = date.today()
        get_year = data[3].split('.')
        day = int(get_year[0])
        month = int(get_year[1])
        year = int(get_year[2])
        age = today.year - year - ((today.month, today.day) < (month, day))
        params = {
            'count': 1000,
            'fields': 'photo_max, has_photo, is_closed',
            'city': data[0]["id"],
            'sex': sex,
            'age_from': age - 3,
            'age_to': age + 3,
            'access_token': self.token,
            'v': 5.131
            }
        res = requests.get(url_info, params=params).json()

        return res
        

    def get_photo(self, id):#функция выгрузки фото с профиля
        photo_all =[]
        photo_3 = []
        num = []
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
            file_likes = values["likes"]["count"]
            id_photo = values["id"]
            file_photo = {'id_photo': id_photo, 'likes': file_likes}
            photo_all.append(file_photo)

        #все лайки переношу в список, сортирую, оставляю 3 самых больших значения
        for links in photo_all:
            num.append(links['likes'])
        n = min(3, len(num))
        max_numbers = sorted(num, reverse=True)[:n]
        for links in photo_all:
            if links['likes'] in max_numbers:
                photo_3.append(links['id_photo'])
        return photo_3

    def get_profile_1(self, user_id):#функция для вызова всех функций
        user_list = self.user_info(user_id)#
        get_info_max_id = self.user_search(user_list)#
        profile_needs = []
        count = 0
        #ДЕЛАЕМ ОТБОР ПО ОТКРЫТОМУ ПРОФИЛЮ И ИМЕЮЩЕЙСЯ ФОТКЕ
        for values in get_info_max_id["response"]["items"]:
            if values["is_closed"] == False and values["has_photo"] == 1:
                profile_needs.append(values)
                count +=1
        #СЮДА ПИШЕМ РАНДОМ ДЛЯ profile_needs
        profile_info = self.extract_random(profile_needs)
        # profile_needs.remove(profile_info) как удалить элемент из списка?
        #ВЫДЕЛЯЕМ ЭЛЕМЕНТЫ ЕДИНИЧНОГО id
        id_person = profile_info["id"]
        #ПОЛУЧАЕМ ЗНАЧЕНИЕ ДЛЯ 3 ФОТО ПО id
        photo_profile = self.get_photo(id_person)
        attachment = []
        for photo in photo_profile:
            attachment_one = f'photo{id_person}_{photo}'
            attachment.append(attachment_one)
        attachment = ','.join(attachment)
        link_id = f'https://vk.com/id{id_person}'
        name = values["first_name"] + ' ' + values["last_name"]
        profile = {'id': id_person, 'name': name, 'link_id': link_id, 'attachment': attachment, 'user_id': user_list[4]}
        return profile#Возвращаем инфу о профиле для вывода в функцию message_send_photo

    def extract_random(self, lst):
        if not lst:
            return None
        index = randrange(len(lst))
        return lst.pop(index)
    
    
    def message_send_photo(self, user_id, bottoken):#функция принимает токен группы и словарь с данными людей
        profile_1 = self.get_profile_1(user_id)
        user_id = profile_1['user_id']#ваш id
        name = profile_1['name']#имя и фамилия челвоека
        link = profile_1['link_id']#ссылка на его профиль
        message = f'{name}\n {link}'
        att = profile_1['attachment']
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

