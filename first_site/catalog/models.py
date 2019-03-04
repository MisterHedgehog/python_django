import random

import django_filters
from django import forms
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Field, BooleanField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from sortedm2m.fields import SortedManyToManyField
from time import gmtime, strftime

from catalog.filters import RangeFilter

COLOR_CHOICES = ((0, 'Красный'), (1, 'Белый'), (2, 'Чёрный'), (3, 'Шоколадный'), (4, 'Хаки'))


def save_image(instance, filename):
    return "{0}/{1}_{2}.{3}".format(instance.name, instance.name, strftime("%Y-%m-%d-%H-%M-%S", gmtime()),
                                    filename.split('.')[-1])


def save_user_image(instance, filename):
    return "{0}/{1}_{2}.{3}".format(instance.user.username, instance.user.username, strftime("%Y-%m-%d-%H-%M-%S", gmtime()),
                                    filename.split('.')[-1])


class Profile(models.Model):
    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили'

    balance = models.IntegerField(verbose_name='Счёт', default=100)
    user = models.OneToOneField(User, verbose_name="Пользователь", on_delete=models.CASCADE, default=1)
    image = models.ImageField(upload_to=save_user_image, default='default.jpg')

    def __str__(self):
        return '{0} {1}'.format(self.pk, self.user.username)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Brand(models.Model):
    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    name = models.CharField(max_length=100, verbose_name='Наименование')

    def __str__(self):
        return '{0} {1}'.format(self.pk, self.name)

    def get_absolute_url(self):
        return reverse('')


class Photo(models.Model):
    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to=save_image)

    def __str__(self):
        return self.name


class Item(models.Model):
    class Meta:
        verbose_name = 'Базовый тавар'
        verbose_name_plural = 'Базовые тавары'

    category_name = 'Базовый тавар'

    name = models.CharField(max_length=120, verbose_name='Наименование', default='Honor 5s')
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name="Продовец", default=1)
    amount = models.IntegerField(verbose_name='на складе', default=1)
    pub_date = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена', default=228)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name='Брэнд', default=1)
    images = SortedManyToManyField(Photo, verbose_name='изображения', default=[1,])
    description = models.TextField(verbose_name='Описание', default='Телефон уан лаф')
    users_comments = models.ManyToManyField(User, through='Comment', verbose_name='Список пользователей')

    def __str__(self):
        return '{0} {1}'.format(self.pk, self.name)

    def add_random_photos(self, amount: int):
        for photo in random.choices(population=Photo.objects.all(), k=amount):
            self.images.add(photo)
        return self

    @classmethod
    def cls(cls):
        return cls

    def get_absolute_url(self):
        return reverse('catalog:item', {'pk': self.pk})

    ###
    # Функция производит обход атрибутов модели, которых следует показывать пользователю
    ###
    def __iter__(self):
        field: Field
        # field имеет тип IntegerField или что-то, что наследуется от Field
        for field in self._meta.fields:
            # tag - имя атрибута, например, name
            tag = str(field).split('.')[-1]
            if tag in ('id', 'description', 'name', 'pub_date', 'item_ptr',
                       'computingdevice_ptr'):
                continue
            if tag in ('cores',):
                yield ('Процессор', '')
            if tag in ('price',):
                yield ('Основное', '')
            if tag in ('diagonal',):
                yield ('Экран', '')
            # val - значение атрибута, например, '2'
            val = field.value_to_string(self)
            if field.choices:
                for (v_id, v) in field.choices:
                    val = v if val == str(v_id) else val
            if tag == 'brand':
                val = Brand.objects.get(pk=val).name
            if tag == 'owner':
                val = User.objects.get(pk=val).username
            if isinstance(field, BooleanField):
                val = {'True': 'Да', 'False': 'Нет'}[val]
            yield (field.verbose_name, val)

    def get_category_id(self):
        cls = get_all_classes()
        for (key, value) in enumerate(cls):
            if value == self.category_name:
                return key
        return 1

    @classmethod
    def get_filter(cls, data):
        class ItemFilter(django_filters.FilterSet):
            class Meta:
                model = cls
                exclude = {'images', 'description', 'pub_date', 'users_comments'}
                filter_overrides = {
                    models.IntegerField: {
                        'filter_class': RangeFilter,
                    },
                    models.DecimalField: {
                        'filter_class': RangeFilter,
                    },
                    models.CharField: {
                        'filter_class': django_filters.CharFilter,
                    },
                }
        return ItemFilter(data=data, queryset=cls.objects.all())

    @classmethod
    def get_form(cls, data=None, instance=None):
        class ItemForm(forms.ModelForm):
            class Meta:
                model = cls
                exclude = ['pub_date', 'users_comments', 'owner']
                # widgets = {
                #     'adv': forms.Textarea(attrs={'class': 'form-control is-invalid', 'rows': 4, }),
                #     'lim': forms.Textarea(attrs={'class': 'form-control is-invalid', 'rows': 4, }),
                #     'mark': forms.Select(attrs={'class': 'custom-select'}),
                #     'text_comment': forms.Textarea(attrs={'class': 'form-control is-invalid', 'rows': 7, }),
                #     'short_comment': forms.Textarea(attrs={'class': 'form-control is-invalid', 'rows': 1, }),
                # }
        return ItemForm(data, instance=instance) if data else ItemForm()

    @classmethod
    def get_subclasses(cls):
        return cls.__subclasses__()


class Clothes(Item):
    SIZE_CHOICES = ((0, 'S'), (1, 'M'), (2, 'L'))
    SEX_CHOICES = ((0, 'Male'), (1, 'Female'))
    MATERIAL_CHOICES = ((0, 'Шерсть'), (1, 'Синтипон'), (2, 'Хлопок'))
    SEASON_CHOICES = ((0, 'Лето'), (1, 'Полу-утеплённый'), (2, 'Утеплённый'), (3, 'Уни-сезонный'))

    class Meta:
        verbose_name = 'Одежда'
        verbose_name_plural = verbose_name

    category_name = Meta.verbose_name_plural

    size = models.IntegerField(verbose_name='размер', choices=SIZE_CHOICES, default=0)
    color = models.IntegerField(verbose_name='цвет', choices=COLOR_CHOICES, default=0)
    sex = models.IntegerField(verbose_name='пол', choices=SEX_CHOICES, default=0)
    material = models.IntegerField(verbose_name='материал', choices=MATERIAL_CHOICES, default=0)
    season = models.IntegerField(verbose_name='сезон', choices=SEASON_CHOICES, default=0)


class Jeans(Clothes):

    class Meta:
        verbose_name = 'Джинсы'
        verbose_name_plural = verbose_name

    category_name = Meta.verbose_name_plural

    is_heavy = models.BooleanField(verbose_name='уплотнённые', default=False)


class Dress(Clothes):

    class Meta:
        verbose_name = 'Платье'
        verbose_name_plural = 'Платья'

    category_name = Meta.verbose_name_plural

    is_curly = models.BooleanField(verbose_name='кучерявое', default=False)
    is_evening = models.BooleanField(verbose_name='вечернее', default=False)


class Hat(Clothes):

    class Meta:
        verbose_name = 'Шляпа'
        verbose_name_plural = 'Шляпы'

    category_name = Meta.verbose_name_plural

    with_field = models.BooleanField(verbose_name='с полями', default=False)


class Processor(models.Model):
    POWER_CHOICES = ((15, '15 Ват'), (30, '30 Ват'), (65, '65 Ват'), (95, '95 Ват'),)

    class Meta:
        abstract = True

    cores = models.IntegerField(verbose_name='Кол ядер', default=2)
    frequency = models.IntegerField(verbose_name='Частота', default=2000)
    turbo_fre = models.IntegerField(verbose_name='Turbo-частота', default=2000)
    power = models.PositiveSmallIntegerField(verbose_name='Энергопотребление', default=65, choices=POWER_CHOICES)


class Display(models.Model):
    DIAGONAL_CHOICES = ((0, 'менее 13'), (1, '14'), (2, 'более 14'))
    RESOLUTION_CHOICES = ((0, 'HD'), (1, 'FullHD'), (2, '4K'))
    TECHNOLOGY_CHOICES = ((0, 'TN'), (1, 'IPS'), (2, 'OLED'))
    SURFACE_CHOICES = ((0, 'глянцовая'), (1, 'матовая'),)

    class Meta:
        abstract = True

    diagonal = models.IntegerField(verbose_name='диагональ экрана', choices=DIAGONAL_CHOICES, default=0)
    resolution = models.IntegerField(verbose_name='разрешение экрана', choices=RESOLUTION_CHOICES, default=0)
    technology = models.IntegerField(verbose_name='технология', choices=TECHNOLOGY_CHOICES, default=0)
    surface = models.IntegerField(verbose_name='поверность', choices=SURFACE_CHOICES, default=0)
    is_sensor = models.BooleanField(verbose_name='сенсорный', default=False)


class ComputingDevice(Item, Display, Processor):
    class Meta:
        verbose_name = 'Вычислительный прибор'
        verbose_name_plural = 'Вычислительные приборы'

    category_name = Meta.verbose_name_plural


class Notebook(ComputingDevice):
    class Meta:
        verbose_name = 'Ноутбук'
        verbose_name_plural = 'Ноутбуки'

    category_name = Meta.verbose_name_plural

    TYPE_CHOICES = ((0, 'универсальный'), (1, 'игровой'))

    type = models.IntegerField(verbose_name='Тип', choices=TYPE_CHOICES, default=0)


class SmartPhone(ComputingDevice):
    class Meta:
        verbose_name = 'Смартфон'
        verbose_name_plural = 'Смартфоны'

    category_name = Meta.verbose_name_plural


class Tablet(ComputingDevice):
    class Meta:
        verbose_name = 'Планшет'
        verbose_name_plural = 'Планшеты'

    category_name = Meta.verbose_name_plural


class Comment(models.Model):
    V_BAD = 'Очень плохо'
    BAD = 'Плохо'
    NORM = 'Сойдёт'
    GOOD = 'Хорошо'
    V_GOOD = 'Отлично'
    MARK_CHOICES = (
        (1, V_BAD),
        (2, BAD),
        (3, NORM),
        (4, GOOD),
        (5, V_GOOD),
    )
    short_comment = models.CharField(max_length=60, verbose_name='Мнение')
    text_comment = models.TextField(verbose_name="Комментарий")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Покупатель')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name='Товар')
    mark = models.IntegerField(verbose_name='Оценка', default=NORM, choices=MARK_CHOICES)
    adv = models.CharField(max_length=120, verbose_name='Достоинства')
    lim = models.CharField(max_length=120, verbose_name='Недостатки')
    date = models.DateField(auto_now=True, verbose_name='Время обновления')

    def __str__(self):
        return 'О товаре: {0}, Покупателя: {1}'.format(self.item.name, self.user.username)


# Функция, находящая класс, который наследуется от класса Item и имеет название category_name
def get_class(category_name):
    def search(cls):
        if cls.category_name == category_name:
            return cls
        for sub_cls in cls.get_subclasses():
            result = search(sub_cls)
            if result is not None:
                return result

    return search(Item)


# Функция, находящая классы, не имеющие наследников
def get_end_classes():
    def search(cls):
        result = []
        if cls.__subclasses__():
            for sub_cls in cls.get_subclasses():
                result += search(sub_cls)
            return result
        else:
            return [cls.category_name, ]
    return search(Item)


# Функция, находящая всех наследников класса Item
def get_all_classes():
    def search(cls):
        result = []
        if cls.__subclasses__():
            result += [cls.category_name, ]
            for sub_cls in cls.get_subclasses():
                result += search(sub_cls)
            return result
        else:
            return [cls.category_name, ]
    return search(Item)


# Функция, находящая объект, который наследуется от класса Item и имеет pk=pk
def get_item_child(pk: int):
    def search(cls):
        if cls.__subclasses__():
            for sub_cls in cls.get_subclasses():
                result = search(sub_cls)
                if result is not None:
                    return result
        try:
            return cls.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return
    return search(Item)

# Common = type('Common', (models.Model,), {})
