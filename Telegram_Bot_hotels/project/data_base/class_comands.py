import time


class LowPrice:
    def __init__(self, date, city):
        self.date = date
        self.city = city
        self.city_id = None
        self.number_hotels = None
        self.list_foto = dict()
        self.price_min = None
        self.price_max = None
        self.checkin = None
        self.checkout = None
        self.deltatime = None
        self.sort_filter = 'PRICE_LOW_TO_HIGH'

    def __str__(self):
        return 'Дешевые отели'

    def __repr__(self):
        return f'{time.strftime("%d-%m-%y %H:%M:%S", time.localtime(self.date))}|LowPrice'


class HighPrice:
    def __init__(self, date, city):
        self.date = date
        self.city = city
        self.city_id = None
        self.number_hotels = None
        self.list_foto = dict()
        self.price_min = None
        self.price_max = None
        self.checkin = None
        self.checkout = None
        self.deltatime = None
        self.sort_filter = '-PRICE_LOW_TO_HIGH'

    def __str__(self):
        return 'Дорогие отели'

    def __repr__(self):
        return f'{time.strftime("%d-%m-%y %H:%M:%S", time.localtime(self.date))}|HighPrice'


class BestDeal:
    def __init__(self, date, city):
        self.date = date
        self.city = city
        self.city_id = None
        self.number_hotels = None
        self.list_foto = dict()
        self.price_min = None
        self.price_max = None
        self.checkin = None
        self.checkout = None
        self.deltatime = None
        self.sort_filter = 'DISTANCE'

    def __str__(self):
        return 'Лучшие предложения'

    def __repr__(self):
        return f'{time.strftime("%d-%m-%y %H:%M:%S", time.localtime(self.date))}|BestDeal'
