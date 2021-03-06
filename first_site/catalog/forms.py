from django import forms

from catalog.models import Comment


# Простейшая форма, отображающая поле для ввода числа
class AmountForm(forms.Form):
    amount = forms.IntegerField(min_value=1, max_value=1000, label='Количество', initial=3)


# Форма, необходимая для созлания комментария к товару
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['short_comment', 'text_comment', 'mark', 'adv', 'lim', ]
        widgets = {
            'adv': forms.Textarea(attrs={'class': 'form-control is-invalid', 'rows': 4, }),
            'lim': forms.Textarea(attrs={'class': 'form-control is-invalid', 'rows': 4, }),
            'mark': forms.Select(attrs={'class': 'custom-select'}),
            'text_comment': forms.Textarea(attrs={'class': 'form-control is-invalid', 'rows': 7, }),
            'short_comment': forms.Textarea(attrs={'class': 'form-control is-invalid', 'rows': 1, }),
        }


