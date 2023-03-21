import pickle

from api.handler_step_poll import get_min_and_max_value
from api.handler_request_api_hotels import get_index_named_city
from data_base.class_comands import BestDeal
from commands.loader import bot, history


def get_city_name_for_bestdeal(message):
    """ Функция поиска лучших предложений.
    Получаем город, инициализируем запрос.

    """
    user = message.chat.id
    date = message.date
    city = message.text
    poll = BestDeal(date, city)
    if user in history:
        user = history[user]
        user.append(poll)
    else:
        history[user] = [poll]
    bot.send_message(message.from_user.id, 'Проверяю....')
    result = get_index_named_city(city)
    poll.city_id = result
    #print(history)
    with open('data_base/history.pickle', 'wb') as f:
        pickle.dump(history, f)
    if not result:
        msg = bot.send_message(message.from_user.id, text='Такого города найти не смог\n'
                                                          'укажите другой город:')
        bot.register_next_step_handler(msg, get_city_name_for_bestdeal)
        return
    bot.send_message(message.from_user.id, 'Хорошо. Продолжим...')
    bot.send_message(message.from_user.id, 'Укажите минимальну и максимальную цену цену через пробел')
    bot.register_next_step_handler(message, get_min_and_max_value)
