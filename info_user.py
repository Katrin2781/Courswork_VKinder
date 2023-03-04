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
            city = value['city']['title']
            sex = value['sex']
            bdate = value['bdate']
            name = value['first_name'] + ' ' + value['last_name']
            user_list = [city, sex, name, bdate]
            print(user_list)

            return user_list
        
    # Используется только Токен персональный
    def get_city_id(self, name):
        url_info = 'https://api.vk.com/method/database.getCities'
        params = {
            'country_id': 1,
            'need_all': 0,
            'q': name,
            'access_token': self.token,
            'v': 5.131
        }
        res = requests.get(url_info, params=params).json()
        id = res["response"]['items'][0]['id']
        return id
       
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
            'city': self.get_city_id(data[0]),
            'sex': sex,
            'age_from': age - 3,
            'age_to': age + 3,
            'access_token': self.token,
            'v': 5.131
            }
        res = requests.get(url_info, params=params).json()
        return res

if __name__== '__main__':
    vk = VkDownloader(bottoken)
    vk_2 = VkDownloader(perstoken)
