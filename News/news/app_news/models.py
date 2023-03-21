from django.db import models
import datetime
from django.contrib.auth.models import User
from django.urls import reverse


class Comments(models.Model):
    user_name = models.CharField(max_length=100, verbose_name='Имя пользователя', blank=True, default='Анонимный пользователь')
    comment = models.CharField(max_length=2000, verbose_name='Комментарий', blank=True)
    user_news = models.ForeignKey('News', blank=True, null=True, on_delete=models.CASCADE, related_name='comments', verbose_name='связь коммента с новостью')
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, blank=True, verbose_name='Зареганый юзер')


    # def __str__(self):
    #     return f' Новость: {self.id}, '

class News(models.Model):
    STATUS_CHOICES = [
        ('A', 'Одобрено'),
        ('N', 'Неактивно')
    ]
    name = models.CharField(max_length=100, verbose_name='Заголовок новости')
    description = models.CharField(max_length=2000, verbose_name='Описание новости')
    create_date = models.DateField(verbose_name='Дата создания', default=datetime.datetime.today)
    edit_date = models.DateField(verbose_name='Дата редактирования', default=datetime.datetime.today)
    is_active = models.CharField(max_length=100, choices=STATUS_CHOICES, default='N')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, verbose_name='Категория')

    def __str__(self):
        return f'{self.name} {self.create_date}'


class Category(models.Model):
    name = models.CharField(max_length=100)
    #slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_id': self.pk})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']
