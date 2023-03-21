from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Profile(models.Model):
    STATUS_CHOICES = [
        ('Шопоголик', '3'),
        ('Покупатель', '2'),
        ('Новичок', '1')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='Новичок')
    points = models.IntegerField(default=0)

    def isstatus(self):
        if self.points <= 10000:
            self.status = 'Новичок'
        elif 10000 <= self.points <= 40000:
            self.status = 'Покупатель'
        else:
            self.status = 'Шопоголик'
    def minus_balance(self, point):
        self.balance -= point

    def plus_point(self, point):
        self.points += point

    def minus_point(self, point):
        self.points -= point

    def __str__(self):
        return f'{self.user} {self.balance} {self.status}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
