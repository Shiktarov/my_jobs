# Generated by Django 2.2 on 2022-12-13 17:32

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_news', '0007_auto_20221213_1432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='user',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Зареганый юзер'),
        ),
        migrations.AlterField(
            model_name='comments',
            name='user_news',
            field=models.ForeignKey(default='id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='app_news.News', verbose_name='связь коммента с новостью'),
        ),
        migrations.AlterField(
            model_name='news',
            name='create_date',
            field=models.DateField(default=datetime.datetime(2022, 12, 13, 17, 32, 1, 864412), verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='news',
            name='edit_date',
            field=models.DateField(default=datetime.datetime(2022, 12, 13, 17, 32, 1, 864460), verbose_name='Дата редактирования'),
        ),
    ]
