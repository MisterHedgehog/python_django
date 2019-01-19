from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models
from django.urls import reverse
from sortedm2m.fields import SortedManyToManyField


class Category(models.Model):

    name = models.CharField(max_length=100, verbose_name='Наименование')
    leaves = models.ManyToManyField('Category', verbose_name="Подкатегории", blank=True)

    class Meta:
        verbose_name = 'Категория'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:category', {'pk': self.pk})

    def get_class_from_category(self, category: str):
        return


class Brand(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('')


def save_image(instance, filename):
    filename = instance.name + '_' + str(instance.pk) + '.' + filename.split('.')[-1]
    return "{0}/{1}".format(instance.name, filename)





class Item(models.Model):
    class Meta:
        verbose_name = 'Базовый тавар'

    category_name = 'Базовые тавары'

    name = models.CharField(max_length=120, verbose_name='Наименование', default='Honor 5s')
    pub_date = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория', blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name='Брэнд')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена', default=228)

    description = models.TextField(verbose_name='Описание', default='Телефон уан лаф')
    users_comments = models.ManyToManyField(User, through='Comment', verbose_name='Список пользователей')

    def __str__(self):
        return '{0} {1}'.format(self.pk, self.name)

    def get_absolute_url(self):
        return reverse('catalog:item', {'pk': self.pk})

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        Category.objects.get_or_create(name=Item.category_name)
        self.category, _ = Category.objects.get_or_create(name=self.category_name)
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)


class Processor(models.Model):
    POWER_CHOICES = ((15, '15 Ват'), (30, '30 Ват'), (65, '65 Ват'), (95, '95 Ват'), )

    class Meta:
        abstract = True

    cores = models.PositiveSmallIntegerField(verbose_name='Кол ядер', default=2)
    frequency = models.IntegerField(verbose_name='Частота', default=2000)
    turbo_fre = models.IntegerField(verbose_name='Turbo-частота', default=2000)
    power = models.IntegerField(verbose_name='Энергопотребление', default=65, choices=POWER_CHOICES)


class Display(models.Model):
    DIAGONAL_CHOICES = ((0, 'менее 13'), (1, '14'), (2, 'более 14'))
    RESOLUTION_CHOICES = ((0, 'HD'), (1, 'FullHD'), (2, '4K'))
    TECHNOLOGY_CHOICES = ((0, 'TN'), (1, 'IPS'), (2, 'OLED'))
    SURFACE_CHOICES = ((0, 'глянцовая'), (1, 'матовая'), )

    class Meta:
        abstract = True

    diagonal = models.PositiveSmallIntegerField(verbose_name='диагональ экрана', choices=DIAGONAL_CHOICES, default=0)
    resolution = models.PositiveSmallIntegerField(verbose_name='разрешение экрана', choices=RESOLUTION_CHOICES, default=0)
    technology = models.PositiveSmallIntegerField(verbose_name='технология', choices=TECHNOLOGY_CHOICES, default=0)
    surface = models.PositiveSmallIntegerField(verbose_name='поверность', choices=SURFACE_CHOICES, default=0)
    is_sensor = models.BooleanField(verbose_name='сенсорный', default=False)


class ComputingDevice(Item, Display, Processor):
    class Meta:
        verbose_name = 'Вычислительный прибор'
    category_name = 'Вычислительные приборы'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        Category.objects.get_or_create(name=ComputingDevice.category_name)
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)


class Notebook(ComputingDevice):
    class Meta:
        verbose_name = 'Ноутбук'
    category_name = 'Ноутбуки'

    TYPE_CHOICES = ((0, 'универсальный'), (1, 'игровой'))

    type = models.IntegerField(verbose_name='Тип', choices=TYPE_CHOICES, default=0)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        Category.objects.get_or_create(name=Notebook.category_name)
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)


class SmartPhone(ComputingDevice):
    class Meta:
        verbose_name = 'Смартфон'
    category_name = 'Смартфоны'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        Category.objects.get_or_create(name=SmartPhone.category_name)
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)


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


CLASSES = {
    cls.category_name: cls for cls in [Item, ComputingDevice, SmartPhone, Notebook]
}
