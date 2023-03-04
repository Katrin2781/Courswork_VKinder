import vk_api
import configparser
from random import randrange
from vk_api.longpoll import VkLongPoll, VkEventType
from info_user import user_info

config = configparser.ConfigParser() 
config.read("settings.ini")
bottoken = config["Tokens"]["vk_group"]
perstoken = config["Tokens"]["vk_pers"]

vk = vk_api.VkApi(token=bottoken)
longpoll = VkLongPoll(vk)


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:


        if event.to_me:

            request = event.text

            if request == "привет":
                write_msg(event.user_id, f"Хай, {event.user_id}")
                user_info(event.user_id, bottoken) #личные данные списком(ИФ, город, пол, дата рождения)

            elif request == "пока":
                write_msg(event.user_id, "Пока((")
            else:
                write_msg(event.user_id, "Не поняла вашего ответа...")


