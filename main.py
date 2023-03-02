#Сюда подтягиваем код:)
#https://github.com/AppLoidx/vk_bot.git
from random import randrange

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

# token = input('Token: ')




def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})

token = ''


vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            request = event.text

            if request == "привет":
                write_msg(event.user_id, f"Хай, {event.user_id}")
            elif request == "пока":
                write_msg(event.user_id, "Пока((")
            else:
                write_msg(event.user_id, "Не поняла вашего ответа...")
