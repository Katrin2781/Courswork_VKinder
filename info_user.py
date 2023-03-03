import requests

def user_info(user_id, token):
    url_info = 'https://api.vk.com/method/users.get'
    params = {
        'user_ids': user_id,
        'fields': 'sex, city, maiden_name',
        'access_token': token,
        'v': 5.131
    }
    res = requests.get(url_info, params=params).json()

    for value in res["response"]:
        city = value['city']['title']
        sex = value['sex']
        name = value['first_name'] + ' ' + value['last_name']
        user_list = [city, sex, name]
        print(user_list)

        return user_list


