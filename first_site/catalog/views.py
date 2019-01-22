import django_filters
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views.generic import FormView

from .models import Item, Comment, Notebook, SmartPhone, get_class, get_item_child
from django.views import generic
from catalog.forms import AmountForm, CommentForm
from django.forms.models import model_to_dict


def redirect_to_catalog(request):
    return HttpResponseRedirect(reverse('catalog:catalog'))


def show_catalog(request):
    items = Item.objects.all()
    data = {
        'items': items,
        'main_class': Item
    }
    return render(request, 'catalog/index.html', data)


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


def delete_item_from_basket(request, pk):
    basket = BaseBasket(request.session)
    basket.delete(pk)
    return HttpResponseRedirect(reverse('catalog:basket'))


def clear_basket(request):
    basket = BaseBasket(request.session)
    basket.clear()
    return HttpResponseRedirect(reverse('catalog:basket'))


def show_basket(request):
    basket = BaseBasket(request.session)
    items = {}
    sum = 0
    for (key, value) in basket.basket.items():
        i = Item.objects.get(pk=key)
        amount = value['quantity']
        price = i.price
        sum += price * amount
        items[key] = dict(name=i.name, price=price, total_price=price * amount, amount=amount, pk=key)
    data = {
        'items': items,
        'basket': basket,
        'sum': sum,
    }
    return render(request, 'catalog/basket.html', data)


def show_item(request, pk):
    if request.method == 'POST':
        form = AmountForm(request.POST)
        if form.is_valid():
            basket = BaseBasket(request.session)
            basket.add(pk, quantity=form.cleaned_data['amount'])
            return HttpResponseRedirect(reverse('catalog:basket'))
    item = get_item_child(pk)
    form = AmountForm()
    comments = Comment.objects.filter(item__pk=pk)
    exist = request.user.is_authenticated and comments.filter(user=request.user).exists()
    data = dict(item=item, form=form, comments=comments, exist=exist, info=item, cat=item.category_name)
    return render(request, 'catalog/item.html', data)


def show_category(request, name):
    filter_class = get_class(category_name=name)
    f = filter_class.get_filter(data=request.GET)
    data = {'category': name,
            'filter': f,
            'main_class': Item
            }
    return render(request, 'catalog/category.html', data)


def logout(request):
    auth.logout(request)
    # Перенаправление на страницу.
    return HttpResponseRedirect(reverse('catalog:catalog'))


class RegisterFormView(FormView):
    form_class = UserCreationForm
    # extra_context = {'categories': Category.objects.all()}
    success_url = "/"
    template_name = "catalog/registration.html"

    def form_valid(self, form):
        # Создаём пользователя, если данные в форму были введены корректно.
        form.save()
        return super(RegisterFormView, self).form_valid(form)


@login_required
def add_comment_to_item(request, pk):
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
    return render(request, 'catalog/create_comment.html',
                  dict(form=form, pk=pk))

