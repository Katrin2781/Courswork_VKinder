import requests
from datetime import date
import configparser
# from main import my_id

user_id = 117971802#введите свой айди, я пока в размышлениях

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
            user_list = [city, sex, name, bdate, user_id]
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


def send_main(user_id):#функция для вызова всех функций
    profile_3 = []
    vk_2 = VkDownloader(perstoken)
    user_list = vk_2.user_info(user_id)#
    get_info_3 = vk_2.user_search(user_list)#
    for values in get_info_3["response"]["items"]:
        id_person = values["id"]
        photo_profile = vk_2.get_photo(id_person)
        attachment = []
        for photo in photo_profile:
            attachment_one = f'photo{id_person}_{photo}'
            attachment.append(attachment_one)
        attachment = ','.join(attachment)
        link_id = f'https://vk.com/id{id_person}'
        name = values["first_name"] + ' ' + values["last_name"]
        profile = {'id': id_person, 'name': name, 'link_id': link_id, 'attachment': attachment, 'user_id': user_list[4]}#
        profile_3.append(profile)
    return profile_3#словарь с данными 3 человеков)

# закомментил для связи с main
# if __name__== '__main__':
#     a = send_main()#вызов функции
#     print(a)



