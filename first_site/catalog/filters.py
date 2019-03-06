import django_filters
from django import forms
from django.db import models
from django.forms import MultiWidget, TextInput, CharField, NumberInput, IntegerField


# кастомный виджет, отображающий два поля для ввода значений
# от и до. Используется при создании диапазона во время сортировки.
class RangeWidget(MultiWidget):
    def __init__(self, width, attrs=None):
        widgets = [NumberInput(attrs={'style': 'border-top-right-radius:0; border-bottom-right-radius:0',
                                      'placeholder': 'от', 'class': 'range'}),
                   NumberInput(attrs={'style': 'border-top-left-radius:0; border-bottom-left-radius:0',
                                      'placeholder': 'до', 'class': 'range'})]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.code, value.number]
        else:
            return ['', '']


# кастомное поле, отображающее два поля для ввода значений
# от и до. Используется при создании диапазона во время сортировки.
class RangeField(forms.MultiValueField):
    def __init__(self, width=100, *args, **kwargs):
        list_fields = [IntegerField(required=False),
                       IntegerField(required=False)]
        super().__init__(list_fields, widget=RangeWidget(width=width), *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            return slice(*data_list)
        return None


# кастомный фильтр, отображающий два поля для ввода значений
# от и до. Используется при создании диапазона во время сортировки.
class RangeFilter(django_filters.Filter):
    field_class = RangeField

    def filter(self, qs, value):
        if value:
            if value.start is not None and value.stop is not None:
                self.lookup_expr = 'range'
                value = (value.start, value.stop)
            elif value.start is not None:
                self.lookup_expr = 'gte'
                value = value.start
            elif value.stop is not None:
                self.lookup_expr = 'lte'
                value = value.stop

        return super().filter(qs, value)


# class ItemFilter(django_filters.FilterSet, type):
#     cl = Item
#
#     def __init__(cls, data=None, queryset=None, request=None, prefix=None):
#         # cls._meta = Notebook
#         super().__init__(data=data, queryset=queryset, request=request, prefix=prefix)
#
#     class Meta:
#         model = Item
#         exclude = {'images', 'description', 'pub_date', 'users_comments', 'category'}
#         filter_overrides = {
#             models.IntegerField: {
#                 'filter_class': RangeFilter,
#             },
#             models.DecimalField: {
#                 'filter_class': RangeFilter,
#             },
#             models.PositiveSmallIntegerField: {
#                 'filter_class': RangeFilter,
#             },
#         }


# class NotebookFilter(ItemFilter):
#     price = RangeFilter()
#
#     class Meta:
#         model = Notebook
#         fields = {'type': ['exact'], 'diagonal': ['exact'], 'brand': ['exact']}
#
#
# class SmartPhoneFilter(ItemFilter):
#     class Meta:
#         model = SmartPhone
#         fields = ['is_sensor', 'resolution', 'price', 'brand']
