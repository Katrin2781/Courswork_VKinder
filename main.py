import vk_api
from random import randrange
from vk_api.longpoll import VkLongPoll, VkEventType
from config_read import bottoken, perstoken
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from DB_vkinder import add_elect,add_blacklist, select_black
from info_user import VkDownloader


vk = vk_api.VkApi(token=bottoken)
longpoll = VkLongPoll(vk)


def write_msg(user_id, message, keyboard=None):
    start = {
        'user_id': user_id,
        'message': message,
        'random_id': randrange(10 ** 7),
    }
    if keyboard != None:#изначально кнопки нет, но если есть, добавляем для формирования сообщения
        start['keyboard'] = keyboard.get_keyboard()
    else:
        start = start
    vk.method('messages.send', start)
    

for event in longpoll.listen():
    vk_ex = VkDownloader(perstoken)
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            request = event.text.lower()
            if request == "привет":
                keyboard = VkKeyboard(one_time=True)#создание одноразовой кнопки старт
                user_info = vk_ex.user_info(event.user_id)
                name = user_info[2].split()[0]
                keyboard.add_button('start', VkKeyboardColor.POSITIVE)
                write_msg(event.user_id, f"Хай, {name}. Я твой личный Бот-знакомств."
                                         f"Могу предложить тебе несколько вариантов."
                                         f"Если ты не против, нажми start", keyboard)
            elif request == "start":
                n_keyboard = VkKeyboard(inline=False)#создание многоразовых кнопок
                n_keyboard.add_button('Следующий', VkKeyboardColor.PRIMARY)
                n_keyboard.add_button('В черный список', VkKeyboardColor.NEGATIVE)
                n_keyboard.add_line()
                n_keyboard.add_button('В избранное', VkKeyboardColor.POSITIVE)
                n_keyboard.add_button('Список избранных', VkKeyboardColor.POSITIVE)
                write_msg(event.user_id, f'Для перехода к следующему профилю нажмите Следующий', n_keyboard)
                num = 1#значение для списка 1 профиля, для подгрузки в info_user нужного листа
                person = vk_ex.message_send_photo(event.user_id, bottoken, num)#вызов функции и вывод пользователя в сообщении
            elif request == "следующий":
                num = 1
                black = False  # пометка об использовании функции
                chosen = False
                person = vk_ex.message_send_photo(event.user_id, bottoken, num)
            elif request == "в избранное":# МЕТОД ДОБАВЛЕНИЯ В ИЗБРАННЫЕ          
                try:
                    if black:
                        write_msg(event.user_id, 'Нужно посмотреть кто там дальше... Нажмите Следующий!')
                    else:
                        add_elect(person)
                        answers = [
                            'Отличный выбор!',
                            'Неплохой вариант!',
                            'Мне тоже нравится!',
                            'У тебя хороший вкус!'
                            ]
                        index = randrange(len(answers))
                        write_msg(event.user_id, answers[index]+'Посмотрим ещё? Нажимай Следующий!')
                        chosen = True
                except NameError:
                    write_msg(
                        event.user_id,
                        'Сегодня мы ещё не видились.'
                        'Сначала нужно выбрать следующего кандидата!'
                        )
            elif request == "список избранных":
                num = 2#значение для списка избранных, для подгрузки в info_user нужного листа
                result = vk_ex.message_send_photo(event.user_id, bottoken, num)
                if not result:
                    write_msg(
                        event.user_id,
                        'У вас пока нет никого в Избранном. Давайте их поищём?'
                        'Нажмите Следующий!'
                        )
            elif request == "в черный список":# МЕТОД ДОБАВЛЕНИЯ В ЧЕРНЫЙ СПИСОК
                try:
                    if chosen:
                        write_msg(
                            event.user_id,
                            'Мы же добавили его в избранное?'
                            )
                    else:
                        black = True
                        data = vk.method("messages.getConversations", {"count": 1})
                        vk_api = vk.get_api()
                        message_id = data['items'][0]['last_message']['id']-1
                        vk_api.messages.delete(delete_for_all=1, message_ids=message_id)
                        answers = [
                            'Мне тоже не понравился этот профиль!',
                            'Я бы тоже так сделал!',
                            'Не в твоём вкусе?'
                            ]
                        index = randrange(len(answers))
                        write_msg(event.user_id, answers[index] + ' Посмотрим ещё? Нажимай Следующий!')
                        add_blacklist(person)
                except NameError:
                    write_msg(
                        event.user_id,
                        'Сегодня мы ещё не видились!'
                        'Сначала нужно выбрать следующего кандидата!'
                        )
            elif request == "нет":
                write_msg(event.user_id, f"Это чат для знакомств, нам больше нечего предложить, досвидания")
            elif request == "пока":
                write_msg(event.user_id, "Пока((")
            else:
                write_msg(event.user_id, "Не понял вашего ответа...")

