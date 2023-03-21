import re
import time
import pickle
import logging
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto

from commands.loader import bot, history
from api.big_text import ANSWER
from api.handler_request_api_hotels import display_result_getting_list_hotels, give_list_photos_of_hotel


def get_min_and_max_value(message):
    """ Принимает знаечение максимальной и минимальной суммы  """

    string = message.text
    user = message.chat.id
    if not all([st.isdigit() for st in string.split()]):
        msg = bot.send_message(message.from_user.id, text='Ошибка: Неверный тип значений.\n(Ожидаются цифры).')
        bot.register_next_step_handler(msg, get_min_and_max_value)
        return
    try:
        min_p, max_p = string.split()
    except Exception:
        msg = bot.send_message(message.from_user.id, text='Ошибка: Неверное количество значений.\n(Ожидается два).')
        bot.register_next_step_handler(msg, get_min_and_max_value)
        return
    poll = history[user][len(history[user]) - 1]
    poll.price_min = min_p
    poll.price_max = max_p
    #print(history)
    logging.info(history)
    with open('data_base/history.pickle', 'wb') as f:
        pickle.dump(history, f)
    bot.send_message(message.from_user.id, 'Укажите планируемые даты посещения в формате\ndd/mm/yy-dd/mm/yy')
    bot.register_next_step_handler(message, get_checkin_checkout)


def get_checkin_checkout(message):
    """ Получение сообщения даты заезда и выезда """

    string = message.text
    user = message.chat.id
    if re.fullmatch('[0123]\d/[01]\d/2[34]-[0123]\d/[01]\d/2[34]', string):
        if all(map(
                lambda lst: 0 < int(lst.split('/')[0]) <= 31 and
                            0 < int(lst.split('/')[1]) <= 12,
                string.split('-'))):
            now = time.localtime()
            checkin = time.strptime(string.split('-')[0], '%d/%m/%y')
            checkout = time.strptime(string.split('-')[1], '%d/%m/%y')
            if now <= checkin < checkout:
                poll = history[user][len(history[user]) - 1]
                poll.checkin = checkin
                poll.checkout = checkout
                poll.deltatime = checkout[7] - checkin[7]
                with open('data_base/history.pickle', 'wb') as f:
                    pickle.dump(history, f)
                msg = bot.send_message(user, text='Введите количество отелей')
                bot.register_next_step_handler(msg, get_amount_hotels)
                return
    msg = bot.send_message(user, text='Ошибка: Неверный тип значений.\n(Ожидаются формат dd/mm/yy-dd/mm/yy).')
    bot.register_next_step_handler(msg, get_checkin_checkout)


def get_amount_hotels(message):
    """ Получает количество отелей для результата """

    number_hotels = message.text
    user = message.chat.id
    if not number_hotels.isdigit() or not 0 < int(number_hotels) <= 25:
        msg = bot.send_message(message.from_user.id, text='Ошибка. Неверное значение. (ожидается цифра не более 25)')
        bot.register_next_step_handler(msg, get_amount_hotels)
        return

    poll = history[user][len(history[user]) - 1]
    poll.number_hotels = number_hotels
    #print(history)
    logging.info(history)
    with open('data_base/history.pickle', 'wb') as f:
        pickle.dump(history, f)
    choice = InlineKeyboardMarkup()
    btns = [InlineKeyboardButton(text=value, callback_data=key) for key, value in ANSWER.items()]
    choice.row(btns[0], btns[1])
    bot.send_message(message.from_user.id, 'Показать фото?', reply_markup=choice)


@bot.callback_query_handler(func=lambda call: call.data in ['yes', 'not'])
def get_answer(call):
    """ получение ответа на вывод фотографий
    Если ответ да, переход запрос на количество фото, затем результат с фото.
    Если ответ нет, переход к выводу результата без фото.
    """

    user = call.from_user.id
    poll = history[user][len(history[user]) - 1]
    if call.data == 'yes':
        msg = bot.send_message(call.from_user.id, text='Укажите количество фото (не более 5):')
        bot.register_next_step_handler(msg, get_photos)
        bot.delete_message(call.message.chat.id, call.message.message_id)
    else:
        for hotel_id, hotel_name, string in display_result_getting_list_hotels(
                town_id=poll.city_id,
                amount_htls=poll.number_hotels,
                sort=poll.sort_filter,
                checkin=poll.checkin,
                checkout=poll.checkout,
                p_from=poll.price_min,
                p_to=poll.price_max):
            poll.list_foto[hotel_id] = [hotel_name]
            with open('data_base/history.pickle', 'wb') as f:
                pickle.dump(history, f)
            bot.send_message(user, text=string, parse_mode='html')
        #print(poll.list_foto)
        logging.info(poll.list_foto)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        return_key = InlineKeyboardMarkup()
        return_key.add(InlineKeyboardButton(text='Главное меню', callback_data='go'))
        bot.send_message(user, text='Доклад закончил...', reply_markup=return_key)


def get_photos(message):
    ''' получаем сообщение количества фотографий и инициализируем запрос.'''


    num_foto = message.text
    user = message.from_user.id
    if not num_foto.isdigit() or not 0 < int(num_foto) <= 5:
        msg = bot.send_message(message.from_user.id, text='Ошибка: Неверное значение.\n(ожидается число не более 5)')
        bot.register_next_step_handler(msg, get_photos)
        return

    poll = history[user][len(history[user]) - 1]
    for hotel_id, hotel_name, string in display_result_getting_list_hotels(
            town_id=poll.city_id,
            amount_htls=poll.number_hotels,
            sort=poll.sort_filter,
            checkin=poll.checkin,
            checkout=poll.checkout,
            p_from=poll.price_min,
            p_to=poll.price_max):
        hotel_foto = give_list_photos_of_hotel(hotel_id, hotel_name, num_foto)
        #print(f'{hotel_id}: {hotel_foto}')
        poll.list_foto[hotel_id] = hotel_foto
        with open('data_base/history.pickle', 'wb') as f:
            pickle.dump(history, f)
        if not hotel_foto[1:]:
            msg = bot.send_message(user, text=string)
            bot.send_message(user,
                             text='Ошибка: Фотографии загрузить не удалось',
                             reply_to_message_id=msg.message_id)
            continue
        list_foto = [InputMediaPhoto(foto) for foto in hotel_foto[1:]]
        bot.send_message(user, text=string, parse_mode='html')
        bot.send_media_group(user, list_foto)
    return_key = InlineKeyboardMarkup()
    return_key.add(InlineKeyboardButton(text='Главное меню', callback_data='go'))
    bot.send_message(user, text='Доклад закончил...', reply_markup=return_key)
