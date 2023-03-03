#Сюда подтягиваем код:)
#https://github.com/AppLoidx/vk_bot.git
from random import randrange
from info_user import user_info

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

# token = input('Token: ')




def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})

token = 'vk1.a.j4jpbOeVpV9nWcbtN23XrY49iU4csIgjfzlzXD1b7tcMy0PHrj36YxMe1q402EcJvEetnMjwcEbJBzVa7tWrsm95Jk9Ybu3BRbLgCSuZlh-Qy5K9CiCieVgDGQQ_CI0kF5htznpnY1JO4pOmtXhqxj2WIPrOSMGj66DQBb_4twaiaEQ8GAs9p0PJsJmPxrLIpX7LIkfHXyZIt9gX4uqW4Q'

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:


        if event.to_me:

            request = event.text

            if request == "привет":
                write_msg(event.user_id, f"Хай, {event.user_id}")
                user_info(event.user_id, token)

            elif request == "пока":
                write_msg(event.user_id, "Пока((")
            else:
                write_msg(event.user_id, "Не поняла вашего ответа...")


