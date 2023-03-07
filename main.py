import vk_api
from random import randrange
from vk_api.longpoll import VkLongPoll, VkEventType
from info_user import VkDownloader
from config_read import bottoken, perstoken
from vk_api.keyboard import VkKeyboard, VkKeyboardColor


vk = vk_api.VkApi(token=bottoken)
longpoll = VkLongPoll(vk)



def write_msg(user_id, message, keyboard=None):
    start = {
        'user_id': user_id,
        'message': message,
        'random_id': randrange(10 ** 7),
    }

    if keyboard != None:
        start['keyboard'] = keyboard.get_keyboard()
    else:
        start = start

    vk.method('messages.send', start)
    

for event in longpoll.listen():
    vk_ex = VkDownloader(perstoken)

    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:

            request = event.text

            if request == "привет":
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button('start', VkKeyboardColor.POSITIVE)
                write_msg(event.user_id, f"Хай, {event.user_id}. Хоте ли бы вы познакомиться с новыми людьми? нажмите start", keyboard)
            elif request == "start":
                n_keyboard = VkKeyboard()
                n_keyboard.add_button('next', VkKeyboardColor.PRIMARY)
                n_keyboard.add_button('elect', VkKeyboardColor.POSITIVE)
                n_keyboard.add_button('ignore', VkKeyboardColor.NEGATIVE)
                write_msg(event.user_id, f'Для перехода к следующему профилю нажмите next', n_keyboard)
                vk_ex.message_send_photo(event.user_id, bottoken)#вызов функции и вывод 3 человек в сообщении
            elif request == "next":
                vk_ex.message_send_photo(event.user_id, bottoken)
            elif request == "elect":
                # МЕТОД ДОБАВЛЕНИЯ В ИЗБРАННЫЕ
                pass
            elif request == "ignor":
                #МЕТОД ДОБАВЛЕНИЯ В ЧЕРНЫЙ СПИСОК
                pass
            elif request == "нет":
                write_msg(event.user_id, f"Это чат для знакомств, нам больше нечего предложить, досвидания")
            elif request == "пока":
                write_msg(event.user_id, "Пока((")
            else:
                write_msg(event.user_id, "Не поняла вашего ответа...")

