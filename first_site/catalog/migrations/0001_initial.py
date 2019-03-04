# Generated by Django 2.1.4 on 2019-02-17 11:08

import catalog.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import sortedm2m.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Бренд',
                'verbose_name_plural': 'Бренды',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_comment', models.CharField(max_length=60, verbose_name='Мнение')),
                ('text_comment', models.TextField(verbose_name='Комментарий')),
                ('mark', models.IntegerField(choices=[(1, 'Очень плохо'), (2, 'Плохо'), (3, 'Сойдёт'), (4, 'Хорошо'), (5, 'Отлично')], default='Сойдёт', verbose_name='Оценка')),
                ('adv', models.CharField(max_length=120, verbose_name='Достоинства')),
                ('lim', models.CharField(max_length=120, verbose_name='Недостатки')),
                ('date', models.DateField(auto_now=True, verbose_name='Время обновления')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Honor 5s', max_length=120, verbose_name='Наименование')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('price', models.DecimalField(decimal_places=2, default=228, max_digits=9, verbose_name='Цена')),
                ('description', models.TextField(default='Телефон уан лаф', verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Базовый тавар',
                'verbose_name_plural': 'Базовые тавары',
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to=catalog.models.save_image)),
            ],
            options={
                'verbose_name': 'Изображение',
                'verbose_name_plural': 'Изображения',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.IntegerField(default=100, verbose_name='Счёт')),
                ('user', models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Профиль пользователя',
                'verbose_name_plural': 'Профили',
            },
        ),
        migrations.CreateModel(
            name='ComputingDevice',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='catalog.Item')),
                ('cores', models.IntegerField(default=2, verbose_name='Кол ядер')),
                ('frequency', models.IntegerField(default=2000, verbose_name='Частота')),
                ('turbo_fre', models.IntegerField(default=2000, verbose_name='Turbo-частота')),
                ('power', models.PositiveSmallIntegerField(choices=[(15, '15 Ват'), (30, '30 Ват'), (65, '65 Ват'), (95, '95 Ват')], default=65, verbose_name='Энергопотребление')),
                ('diagonal', models.IntegerField(choices=[(0, 'менее 13'), (1, '14'), (2, 'более 14')], default=0, verbose_name='диагональ экрана')),
                ('resolution', models.IntegerField(choices=[(0, 'HD'), (1, 'FullHD'), (2, '4K')], default=0, verbose_name='разрешение экрана')),
                ('technology', models.IntegerField(choices=[(0, 'TN'), (1, 'IPS'), (2, 'OLED')], default=0, verbose_name='технология')),
                ('surface', models.IntegerField(choices=[(0, 'глянцовая'), (1, 'матовая')], default=0, verbose_name='поверность')),
                ('is_sensor', models.BooleanField(default=False, verbose_name='сенсорный')),
            ],
            options={
                'verbose_name': 'Вычислительный прибор',
                'verbose_name_plural': 'Вычислительные приборы',
            },
            bases=('catalog.item', models.Model),
        ),
        migrations.AddField(
            model_name='item',
            name='brand',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='catalog.Brand', verbose_name='Брэнд'),
        ),
        migrations.AddField(
            model_name='item',
            name='images',
            field=sortedm2m.fields.SortedManyToManyField(help_text=None, to='catalog.Photo', verbose_name='изображения'),
        ),
        migrations.AddField(
            model_name='item',
            name='users_comments',
            field=models.ManyToManyField(through='catalog.Comment', to=settings.AUTH_USER_MODEL, verbose_name='Список пользователей'),
        ),
        migrations.AddField(
            model_name='comment',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.Item', verbose_name='Товар'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Покупатель'),
        ),
        migrations.CreateModel(
            name='Notebook',
            fields=[
                ('computingdevice_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='catalog.ComputingDevice')),
                ('type', models.IntegerField(choices=[(0, 'универсальный'), (1, 'игровой')], default=0, verbose_name='Тип')),
            ],
            options={
                'verbose_name': 'Ноутбук',
                'verbose_name_plural': 'Ноутбуки',
            },
            bases=('catalog.computingdevice',),
        ),
        migrations.CreateModel(
            name='SmartPhone',
            fields=[
                ('computingdevice_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='catalog.ComputingDevice')),
            ],
            options={
                'verbose_name': 'Смартфон',
                'verbose_name_plural': 'Смартфоны',
            },
            bases=('catalog.computingdevice',),
        ),
        migrations.CreateModel(
            name='Tablet',
            fields=[
                ('computingdevice_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='catalog.ComputingDevice')),
            ],
            options={
                'verbose_name': 'Планшет',
                'verbose_name_plural': 'Планшеты',
            },
            bases=('catalog.computingdevice',),
        ),
    ]
