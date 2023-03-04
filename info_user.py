import requests
from datetime import date
import configparser

config = configparser.ConfigParser() 
config.read("settings.ini")
bottoken = config["Tokens"]["vk_group"]
perstoken = config["Tokens"]["vk_pers"]


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
            user_list = [city, sex, name, bdate]
            print(user_list)
            return user_list

        
    # Используется только Токен персональный
    # def get_city_id(self, name):
    #     url_info = 'https://api.vk.com/method/database.getCities'
    #     params = {
    #         'country_id': 1,
    #         'need_all': 0,
    #         'q': name,
    #         'access_token': self.token,
    #         'v': 5.131
    #     }
    #     res = requests.get(url_info, params=params).json()
    #     id = res["response"]['items'][0]['id']
    #     return id
       
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
            file_url = values["sizes"][-1]["url"]
            file_likes = values["likes"]["count"]
            file_photo = {file_likes: file_url}

            photo_all.append(file_photo)

        #все лайки переношу в список, сортирую, оставляю 3 самых больших значения
        num = []
        for links in photo_all:
            for key, value in links.items():
                num.append(key)
        num.sort()
        num = [num[-1], num[-2], num[-3]]

        #нахожу ссылки на фото по 3 максимальным значениям(умнее не придумал)
        for links in photo_all:
            for key, value in links.items():
                if  key == num[0]:
                    photo_3.append(value)
                elif key == num[1]:
                    photo_3.append(value)
                elif key == num[2]:
                    photo_3.append(value)

        return photo_3


def send_main():#функция для вызова всех функций
    profile_3 = []
    vk_2 = VkDownloader(perstoken)
    user_list = vk_2.user_info(117971802)#
    get_info_3 = vk_2.user_search(user_list)#
    for values in get_info_3["response"]["items"]:
        id = values["id"]
        photo_profile = vk_2.get_photo(id)
        link_id = f'https://vk.com/id{id}'
        name = values["first_name"] + ' ' + values["last_name"]
        profile = [name, link_id, photo_profile]#
        profile_3.append(profile)
    return profile_3#криво возвращает 3 профиля с ИФ+ссылка+3ссылки на фото

#закомментил для связи с main
# if __name__== '__main__':
#     send_main()#вызов функции
#     vk = VkDownloader(bottoken)
#     vk_2 = VkDownloader(perstoken)
#     user_list = vk_2.user_info(117971802)
#     get_info_3 = vk_2.user_search(user_list)
#     for values in get_info_3["response"]["items"]:
#         photo_profile = vk_2.get_photo(id)
#         link_id = f'https://vk.com/id{id}'
#         name = values["first_name"] + ' ' + values["last_name"]


