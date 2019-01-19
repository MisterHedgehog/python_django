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

# from catalog.filters import ItemFilter, NotebookFilter, SmartPhoneFilter
# from .models import Category, Item, Comment, Notebook, SmartPhone, CLASSES
from django.views import generic
# from catalog.forms import AmountForm, CommentForm


def redirect_to_catalog(request):
    return HttpResponseRedirect(reverse('catalog:catalog'))


# def show_catalog(request):
#     categories = Category.objects.all()
#     items = Item.objects.all()
#     data = {
#         'categories': categories,
#         'items': items,
#         'main_category': categories.get(name='Базовые тавары'),
#     }
#     return render(request, 'catalog/index.html', data)
#
#
# class BaseBasket:
#     def __init__(self, session):
#         self.session = session
#         self.basket = self.session['basket'] if self.session.get('basket') else {}
#
#     def __str__(self):
#         return str(self.basket.keys())
#
#     def add(self, pk, quantity=1):
#         if str(pk) in self.basket:
#             self.basket[str(pk)]['quantity'] += quantity
#         else:
#             self.basket[str(pk)] = dict(quantity=quantity)
#         self.save()
#
#     def save(self):
#         self.session['basket'] = self.basket
#         self.session.modified = True
#
#     def delete(self, pk):
#         del self.basket[str(pk)]
#         self.save()
#
#     def clear(self):
#         self.basket = {}
#         self.session['basket'] = {}
#         self.save()
#
#
# def delete_item_from_basket(request, pk):
#     basket = BaseBasket(request.session)
#     basket.delete(pk)
#     return HttpResponseRedirect(reverse('catalog:basket'))
#
#
# def clear_basket(request):
#     basket = BaseBasket(request.session)
#     basket.clear()
#     return HttpResponseRedirect(reverse('catalog:basket'))
#
#
# def show_basket(request):
#     basket = BaseBasket(request.session)
#     items = {}
#     sum = 0
#     for (key, value) in basket.basket.items():
#         i = Item.objects.get(pk=key)
#         amount = value['quantity']
#         price = i.price
#         sum += price * amount
#         items[key] = dict(name=i.name, price=price, total_price=price*amount, amount=amount, pk=key)
#     categories = Category.objects.all()
#     data = {
#         'categories': categories,
#         'items': items,
#         'basket': basket,
#         'sum': sum,
#     }
#     return render(request, 'catalog/basket.html', data)
#
#
# def show_item(request, pk):
#     if request.method == 'POST':
#         form = AmountForm(request.POST)
#         if form.is_valid():
#             basket = BaseBasket(request.session)
#             basket.add(pk, quantity=form.cleaned_data['amount'])
#             return HttpResponseRedirect(reverse('catalog:basket'))
#     categories = Category.objects.all()
#     item = Item.objects.get(pk=pk)
#     form = AmountForm()
#     comments = Comment.objects.filter(item__pk=pk)
#     exist = request.user.is_authenticated and comments.filter(user=request.user).exists()
#     data = dict(categories=categories, item=item, form=form, comments=comments, exist=exist)
#     return render(request, 'catalog/item.html', data)
#
#
# def show_category(request, pk):
#     category = Category.objects.get(pk=pk)
#     categories = Category.objects.all()
#     # items = Notebook.objects.filter(category=category)
#     # f = NotebookFilter(request.GET, queryset=items)
#
#     f = get_filter_from_category(category.name, request)
#     filter_class = CLASSES[category.name]
#     f = ItemFilter(request.GET, filter_class.objects.all())
#     data = {'categories': categories, 'category': category, 'filter': f}
#     return render(request, 'catalog/category.html', data)
#
#
# def logout(request):
#     auth.logout(request)
#     # Перенаправление на страницу.
#     return HttpResponseRedirect(reverse('catalog:catalog'))
#
#
# class RegisterFormView(FormView):
#     form_class = UserCreationForm
#     extra_context = {'categories': Category.objects.all()}
#     success_url = "/"
#     template_name = "catalog/registration.html"
#
#     def form_valid(self, form):
#         # Создаём пользователя, если данные в форму были введены корректно.
#         form.save()
#         return super(RegisterFormView, self).form_valid(form)
#
#
# @login_required
# def add_comment_to_item(request, pk):
#     comment = Comment.objects.filter(user=request.user, item__pk=pk)
#     if request.method == 'POST':
#         form = CommentForm(request.POST, instance=comment[0]) if comment else CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.item = Item.objects.get(pk=pk)
#             comment.user = request.user
#             comment.save()
#             return HttpResponseRedirect(reverse('catalog:item', kwargs={'pk': pk}))
#     categories = Category.objects.all()
#     form = CommentForm(instance=comment[0]) if comment else CommentForm()
#     return render(request, 'catalog/create_comment.html',
#                   dict(categories=categories, form=form, pk=pk))


# def get_filter_from_category(category, request):
#     if category == 'Ноутбуки':
#         return NotebookFilter(request.GET, Notebook.objects.all())
#     if category == 'Смартфоны':
#         return SmartPhoneFilter(request.GET, SmartPhone.objects.all())
#     return ItemFilter(request.GET, Item.objects.all())

# def get_filter_from_category(request, pk,diag_size):
#     cat = category.objects.filter(pk = pkm  diag_size = diag_size)
#     if category == 'ноутбуки':
#         return NotebookFilter(request.GET, Notebook.objects.all())
#     elif category == 'смартфоны':
#         return SmartPhoneFilter(request.GET, SmartPhone.objects.all())
#     else:
#         return ItemFilter(request.GET, Item.objects.all())

