import django_filters

from catalog.forms import PhoneField
# from catalog.models import Item, Notebook, SmartPhone


class RangeFilter(django_filters.Filter):
    field_class = PhoneField

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


# class ItemFilter(django_filters.FilterSet):
#
#     class Meta:
#         model = Item
#         exclude = {'image'}
#
#
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
