# Generated by Django 2.2 on 2022-12-06 16:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=2000)),
                ('create_date', models.DateField()),
                ('edit_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=100)),
                ('comment', models.CharField(max_length=2000)),
                ('user_news', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='app_news.News', verbose_name='связь коммента с новостью')),
            ],
        ),
    ]
