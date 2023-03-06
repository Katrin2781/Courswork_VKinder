import vk_api
from random import randrange
from vk_api.longpoll import VkLongPoll, VkEventType
from info_user import VkDownloader
from config_read import bottoken, perstoken


vk = vk_api.VkApi(token=bottoken)
longpoll = VkLongPoll(vk)


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})
    

for event in longpoll.listen():
    vk_ex = VkDownloader(perstoken)

    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:

            request = event.text

            if request == "привет":

                write_msg(event.user_id, f"Хай, {event.user_id}. Хоте ли бы вы познакомиться с новыми людьми? Напишите да/нет")
            elif request == "да":
                vk_ex.message_send_photo(event.user_id, bottoken)#вызов функции и вывод 3 человек в сообщении
            elif request == "следующий":
                vk_ex.message_send_photo(event.user_id, bottoken)
            elif request == "нет":
                write_msg(event.user_id, f"Это чат для знакомств, нам больше нечего предложить, досвидания")
            elif request == "пока":
                write_msg(event.user_id, "Пока((")
            else:
                write_msg(event.user_id, "Не поняла вашего ответа...")

