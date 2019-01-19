from django import forms
from django.forms import MultiWidget, TextInput, CharField, NumberInput, IntegerField

# from catalog.models import Comment, Category


class PhoneWidget(MultiWidget):
    def __init__(self, width, attrs=None):
        widgets = [NumberInput(attrs={'style': 'border-top-right-radius:0; border-bottom-right-radius:0',
                                      'placeholder': 'от', 'class': 'range'}),
                   NumberInput(attrs={'style': 'border-top-left-radius:0; border-bottom-left-radius:0',
                                      'placeholder': 'до', 'class': 'range'})]
        super(PhoneWidget, self).__init__(widgets, attrs)


    def decompress(self, value):
        if value:
            return [value.code, value.number]
        else:
            return ['', '']


class PhoneField(forms.MultiValueField):
    def __init__(self, width=100, *args, **kwargs):
        list_fields = [IntegerField(required=False),
                       IntegerField(required=False)]
        super(PhoneField, self).__init__(list_fields, widget=PhoneWidget(width=width), *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            return slice(*data_list)
        return None


class AmountForm(forms.Form):
    amount = forms.IntegerField(min_value=1, max_value=10, label='Количество')
    number_range = PhoneField(width=100, label='Диапозон')


# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ['short_comment', 'text_comment', 'mark', 'adv', 'lim', ]
#         widgets = {
#             'adv': forms.Textarea(attrs={'class': 'form-control is-invalid', 'rows': 4, }),
#             'lim': forms.Textarea(attrs={'class': 'form-control is-invalid', 'rows': 4, }),
#             'mark': forms.Select(attrs={'class': 'custom-select'}),
#             'text_comment': forms.Textarea(attrs={'class': 'form-control is-invalid', 'rows': 7, }),
#             'short_comment': forms.Textarea(attrs={'class': 'form-control is-invalid', 'rows': 1, }),
#         }


