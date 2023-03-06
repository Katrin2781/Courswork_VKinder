from info_user import VkDownloader

def get_profile_3(user_id, bottoken, perstoken):#функция для вызова всех функций
    vk = VkDownloader(bottoken)
    vk_2 = VkDownloader(perstoken)#создание объекта
    user_list = vk.user_info(user_id)#вызов функции с персональными данными
    user_list2 = vk_2.user_info(user_id)
    get_info_3 = vk_2.user_search(user_list2)#вызов функции с 3 id пользователей
    profile_3 = []
    print(get_info_3)
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
