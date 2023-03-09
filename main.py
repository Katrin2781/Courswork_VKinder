import vk_api
from random import randrange
from vk_api.longpoll import VkLongPoll, VkEventType
from config_read import bottoken, perstoken
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from DB_vkinder import add_elect
from info_user import VkDownloader

vk = vk_api.VkApi(token=bottoken)
longpoll = VkLongPoll(vk)


def write_msg(user_id, message, keyboard=None):
    start = {
        'user_id': user_id,
        'message': message,
        'random_id': randrange(10 ** 7),
    }
    #изначально кнопки нет, но если есть, добавляем для формирования сообщения
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
                keyboard = VkKeyboard(one_time=True)#создание одноразовой кнопки старт
                keyboard.add_button('start', VkKeyboardColor.POSITIVE)
                write_msg(event.user_id, f"Хай, {event.user_id}. Хоте ли бы вы познакомиться с новыми людьми? нажмите start", keyboard)
            elif request == "start":
                n_keyboard = VkKeyboard()#создание многоразовых кнопок
                n_keyboard.add_button('next', VkKeyboardColor.PRIMARY)
                n_keyboard.add_button('elect', VkKeyboardColor.POSITIVE)
                n_keyboard.add_button('elect list', VkKeyboardColor.SECONDARY)
                write_msg(event.user_id, f'Для перехода к следующему профилю нажмите next', n_keyboard)
                num = 1#значение для списка 1 профиля, для подгрузки в info_user нужного листа
                person = vk_ex.message_send_photo(event.user_id, bottoken, num)#вызов функции и вывод пользователя в сообщении

            elif request == "next":
                num = 1
                person = vk_ex.message_send_photo(event.user_id, bottoken, num)
            elif request == "elect":
                # МЕТОД ДОБАВЛЕНИЯ В ИЗБРАННЫЕ
                try:
                    add_elect(person)
                except NameError:
                    write_msg(event.user_id, 'Сначала нужно выбрать следующего кандидата!')
            elif request == "elect list":
                num = 2#значение для списка избранных, для подгрузки в info_user нужного листа
                vk_ex.message_send_photo(event.user_id, bottoken, num)
            elif request == "нет":
                write_msg(event.user_id, f"Это чат для знакомств, нам больше нечего предложить, досвидания")
            elif request == "пока":
                write_msg(event.user_id, "Пока((")
            else:
                write_msg(event.user_id, "Не поняла вашего ответа...")

