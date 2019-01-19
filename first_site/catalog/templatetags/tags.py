from django.template.defaultfilters import register


@register.filter(name='times')
def times(number):
    return range(number)


@register.filter(name='add_num')
def add_num(string, number):
    return '{}{}'.format(string, number)


@register.filter(name='mul')
def mul(num1, num2):
    return num1*num2


@register.filter(name='del')
def delete(num1, num2):
    return num1/num2


@register.filter(name='to_str')
def to_str(num):
    return str(num)


@register.filter(name='contains')
def contains(s: str, sub: str):
    return sub in s
