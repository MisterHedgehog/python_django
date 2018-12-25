import datetime
from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Unit(models.Model):
    name = models.CharField(max_length=200, verbose_name='Величина')
    description = models.CharField(max_length=200, verbose_name='Комментарий', default='Здесь комментарий',
                                   help_text='Место для комментарий')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='Наименование')
    name.short_description = 'Наименование'
    weight = models.IntegerField()
    taste = models.CharField(max_length=200)
    calories = models.IntegerField(default=10)
    color = models.IntegerField(default=0)
    storage_time = models.TimeField(verbose_name='Время хранения')
    unit = models.ManyToManyField(Unit, help_text='Выберите величину')

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    quantity = models.IntegerField()
    unit = models.ManyToManyField(Unit, help_text='Выберите величину')

    def __str__(self):
        return self.name

    def get_amount(self):
        return ' '.join((str(self.quantity), self.unit))
