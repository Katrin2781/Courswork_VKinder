import requests
from random import randrange
from get_profile_3 import get_profile_3


def message_send_photo(user_id, bottoken, perstoken):#функция принимает токен группы и словарь с данными людей
    profile_3 = get_profile_3(user_id, perstoken)
    for info in profile_3:#распаковываем словарь, присваивая значения из него
        user_id = info['user_id']#ваш id
        name = info['name']#имя и фамилия челвоека
        link = info['link_id']#ссылка на его профиль
        message = f'{name}\n {link}'
        att = info['attachment']
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

