import requests
from datetime import date
from DB_vkinder import insert_user

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

            insert_user(user_list)
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
            'count': 3,
            'fields': 'photo_max',
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
        url_photo = 'https://api.vk.com/method/photos.getProfile'
        params = {
            'owner_id': id,
            'album_id': 'profile',
            'extended': 1,
            'photo_sizes': 0,
            'access_token': self.token,
            'v': 5.131
        }
        res = requests.get(url_photo, params=params).json()

        photo_all =[]
        photo_3 = []
        #находим ссылки на фото и количество лайков, создаем словари и добавляем их в списко
        for values in res["response"]["items"]:
            file_likes = values["likes"]["count"]
            id_photo = values["id"]
            file_photo = {'id_photo': id_photo, 'likes': file_likes}
            photo_all.append(file_photo)

        #все лайки переношу в список, сортирую, оставляю 3 самых больших значения
        num = []
        for links in photo_all:
            num.append(links['likes'])
        num.sort()
        num = [num[-1], num[-2], num[-3]]
        #нахожу id на фото по 3 максимальным значениям(умнее не придумал)

        for links in photo_all:
            if links['likes'] == num[0]:
                photo_3.append(links['id_photo'])
            elif links['likes'] == num[1]:
                photo_3.append(links['id_photo'])
            elif links['likes'] == num[2]:
                photo_3.append(links['id_photo'])

        return photo_3




