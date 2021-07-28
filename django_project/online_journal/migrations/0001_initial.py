# Generated by Django 3.2.4 on 2021-07-14 14:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='заголовок')),
                ('text', models.TextField(verbose_name='текст поста')),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='дата публикации')),
                ('is_active', models.BooleanField(default=True, verbose_name='статья отображается на сайте')),
                ('views_count', models.IntegerField(default=0, verbose_name='количество просмотров')),
            ],
        ),
    ]
