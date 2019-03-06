from django.contrib import admin
from django.urls import include, path

from catalog import views

app_name = 'catalog'

urlpatterns = [
    path('', views.redirect_to_catalog, name='base'),  # Перенаправляет на catalog/
    path('logout/', views.logout, name='logout'),
    path('', include('django.contrib.auth.urls')),
    path('catalog/', views.show_catalog, name='catalog'),  # Главная страница
    path('basket/', views.show_basket, name='basket'),  # Отображение корзины
    path('basket/<int:pk>/delete/', views.delete_item_from_basket, name='delete_from_basket'),  # Удаление товара из корзины
    path('basket/delete/', views.clear_basket, name='clear_basket'),  # Удаление всех товаров из корзины
    # path('basket/add', views.show_item, name='add_item_in_basket'),
    path('pre_deal/', views.show_deal, name='confirm_deal'),  # Страница со списков всех товаров, которые будут куплены
    path('deal/', views.make_deal, name='make_deal'),  # Осуществление договора
    path('item/<int:pk>/', views.show_item, name='item'),  # Страница товара
    path('item/<int:pk>/add_comment', views.add_comment_to_item, name='add_comment_to_item'),  # Страница с формой добавления комментария к товару
    path('item/select/add', views.select_category_before_add_item, name='select_category_before_add'),  # Страница со списком доступных категорий
    path('item/<int:category>/add', views.add_item_to_database, name='add_item_to_database'),  # Страница с форой добавления товара
    path('category/<int:category_id>/', views.show_category, name='category'),  # Страница категории
    path('reg/', views.RegisterFormView.as_view(), name='registration'),
    path('profile', views.show_profile, name='profile')  # Страница пользователя
]
