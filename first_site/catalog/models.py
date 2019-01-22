import django_filters
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import IntegerField, Field, BooleanField
from django.urls import reverse
from sortedm2m.fields import SortedManyToManyField
from time import gmtime, strftime

from catalog.filters import RangeFilter


class Brand(models.Model):

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    name = models.CharField(max_length=100, verbose_name='Наименование')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('')


def save_image(instance, filename):
    return "{0}/{1}_{2}.{3}".format(instance.name, instance.name, strftime("%Y-%m-%d-%H-%M-%S", gmtime()), filename.split('.')[-1])


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
    pub_date = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена', default=228)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name='Брэнд')
    images = SortedManyToManyField(Photo, verbose_name='изображения')
    description = models.TextField(verbose_name='Описание', default='Телефон уан лаф')
    users_comments = models.ManyToManyField(User, through='Comment', verbose_name='Список пользователей')

    def __str__(self):
        return '{0} {1}'.format(self.pk, self.name)

    @classmethod
    def cls(cls):
        return cls

    def get_absolute_url(self):
        return reverse('catalog:item', {'pk': self.pk})

    ###
    # Функция производит обход атрибутов модели, которых следует показывать пользователю
    ###
    def __iter__(self):
        field:Field
        # field имеет тип IntegerField или что-то, что наследуется от Field
        for field in self._meta.fields:
            # tag - имя атрибута, например, name
            tag = str(field).split('.')[-1]
            if tag in ('id', 'description', 'name', 'pub_date', 'item_ptr', 'category',
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
            if isinstance(field, BooleanField):
                val = {'True': 'Да', 'False': 'Нет'}[val]
            yield (field.verbose_name, val)

    @classmethod
    def get_filter(cls, data):
        class ItemFilter(django_filters.FilterSet):
            class Meta:
                model = cls
                exclude = {'images', 'description', 'pub_date', 'users_comments', 'category'}
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
    def get_subclasses(cls):
        return cls.__subclasses__()


class Processor(models.Model):
    POWER_CHOICES = ((15, '15 Ват'), (30, '30 Ват'), (65, '65 Ват'), (95, '95 Ват'), )

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
    SURFACE_CHOICES = ((0, 'глянцовая'), (1, 'матовая'), )

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


def get_class(category_name):
    def search(cls):
        if cls.category_name == category_name:
            return cls
        for sub_cls in cls.get_subclasses():
            result = search(sub_cls)
            if result is not None:
                return result
    return search(Item)


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
