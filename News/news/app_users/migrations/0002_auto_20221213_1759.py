# Generated by Django 2.2 on 2022-12-13 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='phone_number',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='sale_card',
            field=models.IntegerField(null=True),
        ),
    ]
