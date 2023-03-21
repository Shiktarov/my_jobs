import os
import pickle
import telebot
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

__token = os.environ.get("TOKEN")
RapidAPI_Key = os.environ.get("RapidAPI_Key")

bot = telebot.TeleBot(__token)


if os.path.isfile('data_base/history.pickle'):
    with open('data_base/history.pickle', 'rb') as f:
        try:
            history = pickle.load(f)
        except Exception:
            history = dict()
else:

    history = dict()


#print(history)
