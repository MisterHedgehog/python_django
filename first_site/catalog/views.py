import django_filters
from django.contrib import auth
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core import mail
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views.generic import FormView
from django.core.paginator import Paginator

from .models import Item, Comment, Notebook, SmartPhone, get_class, get_item_child, get_end_classes, get_all_classes, Tablet, Profile
from catalog.forms import AmountForm, CommentForm
import random
from django.core.mail import EmailMessage


def redirect_to_catalog(request):
    return HttpResponseRedirect(reverse('catalog:catalog'))


def show_catalog(request):  # catalog/
    if request.method == 'POST':
        form = AmountForm(request.POST)
        if form.is_valid():
            for i in range(form.cleaned_data['amount']):
                item = random.choice([Notebook, SmartPhone, Tablet]).objects.create()
                item.add_random_photos(amount=3)
    all_items = Item.objects.all()[:1000]
    paginator = Paginator(all_items, 24)
    page = request.GET.get('page')
    items = paginator.get_page(page)
    form = AmountForm()
    data = dict(items=items, main_class=Item, form=form)
    return render(request, 'catalog/index.html', add_to_data_total_price_and_quantity(request, data))


class BaseBasket:
    def __init__(self, session):
        self.session = session
        self.basket = self.session['basket'] if self.session.get('basket') else {}

    def __str__(self):
        return str(self.basket.keys())

    def add(self, pk, quantity=1):
        if str(pk) in self.basket:
            self.basket[str(pk)]['quantity'] += quantity
        else:
            self.basket[str(pk)] = dict(quantity=quantity)
        self.save()

    def update(self, pk, quantity=1):
        if str(pk) in self.basket:
            self.basket[str(pk)]['quantity'] = quantity
        else:
            self.basket[str(pk)] = dict(quantity=quantity)
        self.save()

    def save(self):
        self.session['basket'] = self.basket
        self.session.modified = True

    def delete(self, pk):
        del self.basket[str(pk)]
        self.save()

    def clear(self):
        self.basket = {}
        self.session['basket'] = {}
        self.save()

    def get_total_price(self):
        sum = 0
        for (key, value) in self.basket.items():
            i = Item.objects.get(pk=key)
            amount = value['quantity']
            price = i.price
            sum += price * amount
        return sum

    def get_total_quantity(self):
        sum = 0
        for (key, value) in self.basket.items():
            amount = value['quantity']
            sum += amount
        return sum

    def make_deal_and_delete(self, customer: Profile):
        items = {}
        for (key, value) in self.basket.items():
            i = Item.objects.get(pk=key)
            amount = value['quantity']
            price = i.price * amount
            customer.balance -= price
            i.owner.balance += price
            items[i.name] = dict(amount=amount, price=price)
            i.owner.save()
        customer.save()
        self.clear()
        return items


def delete_item_from_basket(request, pk):  # basket/<int:pk>/delete/
    basket = BaseBasket(request.session)
    basket.delete(pk)
    return HttpResponseRedirect(reverse('catalog:basket'))


def clear_basket(request):  # basket/delete/
    basket = BaseBasket(request.session)
    basket.clear()
    return HttpResponseRedirect(reverse('catalog:basket'))


def add_to_data_total_price_and_quantity(request, data=None):
    if data is None:
        data = {}
    basket = BaseBasket(request.session)
    price_sum = basket.get_total_price()
    quantity_sum = basket.get_total_quantity()
    data.update(dict(price_sum=price_sum, quantity_sum=quantity_sum, main_class=Item))
    return data


def show_basket(request):  # basket/
    basket = BaseBasket(request.session)
    items = {}
    sum = 0
    if request.POST:
        form = AmountForm(request.POST)
        if form.is_valid():
            basket = BaseBasket(request.session)
            basket.update(request.POST.get('counter'), quantity=form.cleaned_data['amount'])
    for (key, value) in basket.basket.items():
        i = Item.objects.get(pk=key)
        amount = value['quantity']
        price = i.price
        sum += price * amount
        form = AmountForm(initial={'amount': amount})
        items[key] = dict(name=i.name, price=price, total_price=price * amount, amount=amount, pk=key, form=form)
    data = dict(items=items, basket=basket, sum=sum)
    return render(request, 'catalog/basket.html', add_to_data_total_price_and_quantity(request, data))


@login_required
def make_deal(request):  # deal/
    connection = mail.get_connection()
    # Manually open the connection
    connection.open()
    basket = BaseBasket(request.session)
    items = basket.make_deal_and_delete(request.user.profile)
    table = '{0:^30}{1:^10}{2:^10}\n'.format('название', 'кол.', 'цена')
    total_price = 0
    for item_name in items:
        table += '{0:^30}{1:^10}{2:^10}\n'.format(item_name, items[item_name]['amount'], items[item_name]['price'])
        total_price += items[item_name]['price']
    table += '{0:>50}\n'.format('Итого:  {0}'.format(total_price))
    user_name = request.user.username

    title = "Удачное совершение покупки на сайте BoxMarket!"
    body = """
    Доброго времени суток, {0}
    
        Результат совершённой Вами покупки:
    
{1}       
    
    Благодарим за покупку, команда BoxMarket.
    """.format(user_name, table)
    email = EmailMessage(title, body, to=[request.user.email], connection=connection)
    email.send()
    connection.close()
    return render(request, 'catalog/success_deal.html', add_to_data_total_price_and_quantity(request))


@login_required
def show_deal(request):  # pre_deal/
    basket = BaseBasket(request.session)
    items = {}
    sum = 0
    for (key, value) in basket.basket.items():
        i = Item.objects.get(pk=key)
        amount = value['quantity']
        price = i.price
        sum += price * amount
        items[key] = dict(name=i.name, price=price, total_price=price * amount, amount=amount, pk=key)
    balance = request.user.profile.balance
    data = dict(items=items, basket=basket, sum=sum, balance=balance)
    return render(request, 'catalog/deal.html', add_to_data_total_price_and_quantity(request, data))


def show_item(request, pk):  # item/<int:pk>/
    if request.method == 'POST':
        form = AmountForm(data=request.POST)
        if form.is_valid():
            basket = BaseBasket(request.session)
            basket.add(pk, quantity=form.cleaned_data['amount'])
            return HttpResponseRedirect(reverse('catalog:basket'))
    item = get_item_child(pk)
    form = AmountForm()
    comments = Comment.objects.filter(item__pk=pk)
    exist = request.user.is_authenticated and comments.filter(user=request.user).exists()
    data = dict(item=item, form=form, comments=comments, exist=exist, info=item, cat=item.category_name,)
    return render(request, 'catalog/item.html', add_to_data_total_price_and_quantity(request, data))


def show_category(request, category_id):  # category/<int:category_id>/
    global name
    cls: dict = get_all_classes()
    for (key, value) in enumerate(cls):
        if key == category_id:
            name = value
    filter_class = get_class(category_name=name)
    f = filter_class.get_filter(data=request.GET)
    items_list = f.qs
    pagination = Paginator(items_list, 24)
    page = request.GET.get('page')
    items = pagination.get_page(page)
    data = dict(category=name, filter=f, main_class=Item, items=items)
    return render(request, 'catalog/category.html', add_to_data_total_price_and_quantity(request, data))


def logout(request):  # logout/
    auth.logout(request)
    # Перенаправление на страницу.
    return HttpResponseRedirect(reverse('catalog:catalog'))


class RegisterFormView(FormView):  # reg/
    form_class = UserCreationForm
    # extra_context = {'categories': Category.objects.all()}
    success_url = "/"
    template_name = "catalog/registration.html"

    def form_valid(self, form):
        # Создаём пользователя, если данные в форму были введены корректно.
        form.save()
        return super(RegisterFormView, self).form_valid(form)


@login_required
def add_comment_to_item(request, pk):  # item/<int:pk>/add_comment
    comment = Comment.objects.filter(user=request.user, item__pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment[0]) if comment else CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.item = Item.objects.get(pk=pk)
            comment.user = request.user
            comment.save()
            return HttpResponseRedirect(reverse('catalog:item', kwargs={'pk': pk}))
    form = CommentForm(instance=comment[0]) if comment else CommentForm()
    data = dict(form=form, pk=pk, price_sum=BaseBasket(request.session).get_total_price())
    return render(request, 'catalog/create_comment.html', add_to_data_total_price_and_quantity(request, data))


@login_required
def add_item_to_database(request, category):  # item/<int:category>/add
    category_name = get_end_classes()[category]
    form_class = get_class(category_name=category_name)
    if request.method == 'POST':
        form: forms.ModelForm = form_class.get_form(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.owner = request.user.profile
            item.save()
            return HttpResponseRedirect(reverse('catalog:profile'))
    else:
        form = form_class.get_form()
    data = dict(form=form, category=category, fc=form_class)
    return render(request, 'catalog/add_item.html', add_to_data_total_price_and_quantity(request, data))


@login_required
def select_category_before_add_item(request):  # item/select/add
    selected = 0
    if request.method == 'POST':
        selected = request.POST['category']
        return redirect('catalog:add_item_to_database', selected)
    cls = get_end_classes()
    data = dict(cls=cls, selected=selected, price_sum=BaseBasket(request.session).get_total_price())
    return render(request, 'catalog/categories_of_items.html', add_to_data_total_price_and_quantity(request, data))


@login_required
def show_profile(request):  # profile
    profile: Profile = request.user.profile
    all_items = Item.objects.filter(owner=profile)
    paginator = Paginator(all_items, 24)
    page = request.GET.get('page')
    items = paginator.get_page(page)
    data = dict(profile=profile, items=items, main_class=Item, price_sum=BaseBasket(request.session).get_total_price())
    return render(request, 'catalog/profile.html', add_to_data_total_price_and_quantity(request, data))

