from telebot.types import Message, BotCommand, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from api.big_text import ATTENTION
from commands import lowprice, highprice, bestdeal, history
from api.big_text import DESCRIPTION, HELP_ANSWER, GEN_KEYB
from commands.loader import bot


@bot.message_handler(commands=['start'])
def process_start(message: BotCommand) -> None:
    """
    Оформление приветственного меню с возможностью выбора одного из двух действий:
    - просмотра помощи по командам чата
    - приступить к работе бота

    :param message: команда инициализации бота (/start)
    :return: Команды кнопок Помощь, Начало работы
    """
    bot.send_message(message.from_user.id, 'Привет\n'+DESCRIPTION)
    greeting = InlineKeyboardMarkup()
    btns = [InlineKeyboardButton(text=GEN_KEYB[key], callback_data=key) for key in ['help', 'go']]
    greeting.row(btns[0], btns[1])
    bot.send_message(message.from_user.id, text='Вы можете:', reply_markup=greeting)


@bot.message_handler(commands=['help'])
def text_command_chat(message: BotCommand) -> None:
    """
    Оформление меню 'помощь'
    :param message: команда инициализации бота (/help)
    :return: Сообщение о возможных командах
    """
    helpkey = InlineKeyboardMarkup()
    helpkey.add(InlineKeyboardButton(text='Начать работу', callback_data='go'))
    bot.send_message(message.from_user.id, text=HELP_ANSWER, reply_markup=helpkey)


@bot.callback_query_handler(func=lambda call: call.data in ['go', 'help'])
def run_maim_menu(call):

    """ Выбор команды из меню   """

    if 'help' in call.data:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        start_work = InlineKeyboardMarkup()
        start_work.add(InlineKeyboardButton(text='Начать работу', callback_data='go'))
        bot.send_message(call.from_user.id, text=HELP_ANSWER, reply_markup=start_work)

    elif 'go' in call.data:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        main_menu = InlineKeyboardMarkup()
        buttons = [InlineKeyboardButton(text=GEN_KEYB[key], callback_data=key) for key in [
            'lowprice', 'highprice', 'bestdeal', 'history']]
        main_menu.row(buttons[0], buttons[1]).row(buttons[2], buttons[3])
        bot.send_message(call.from_user.id, text='Выберите действие для просмотра:', reply_markup=main_menu)


@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal', 'history'])
def get_text_command_bestdeal(message):
    """ Принимает команду текстово для выполнения функции"""

    if 'lowprice' in message.text:
        command = lowprice.get_city_name_for_lowprice
        txt = '<b>Выбраны дешёвые отели</b>'

    elif 'highprice' in message.text:
        command = highprice.get_city_name_for_highprice
        txt = '<b>Выбраны дорогие отели</b>'

    elif 'bestdeal' in message.text:
        command = bestdeal.get_city_name_for_bestdeal
        txt = '<b>Выбраны лучшие предложения</b>'

    else:
        msg = bot.send_message(message.from_user.id, text='Сейчас проверю...')
        history.display_history(msg)
        return

    bot.send_message(message.from_user.id, ATTENTION)
    bot.send_message(message.from_user.id, text=txt, parse_mode='html')
    msg = bot.send_message(message.from_user.id, text='Укажите город для поиска')
    bot.register_next_step_handler(msg, command)


@bot.callback_query_handler(func=lambda call: call.data in ['lowprice', 'highprice', 'bestdeal', 'history'])
def start_keyb_command(call):
    """ Выбор команды из меню для получение запроса"""

    if 'lowprice' in call.data:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        command = lowprice.get_city_name_for_lowprice
        txt = '<b>Выбраны дешёвые отели</b>'

    elif 'highprice' in call.data:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        command = highprice.get_city_name_for_highprice
        txt = '<b>Выбраны дорогие отели</b>'

    elif 'bestdeal' in call.data:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        command = bestdeal.get_city_name_for_bestdeal
        txt = '<b>Выбраны лучшие предложения</b>'

    else:
        msg = bot.send_message(call.from_user.id, text='Сейчас проверю...')
        history.display_history(msg)
        return

    bot.send_message(call.from_user.id, ATTENTION)
    bot.send_message(call.from_user.id, text=txt, parse_mode='html')
    msg = bot.send_message(call.from_user.id, text='Укажите город для поиска')
    bot.register_next_step_handler(msg, command)
