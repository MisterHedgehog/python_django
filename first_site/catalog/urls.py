from django.contrib import admin
from django.urls import include, path

from catalog import views

app_name = 'catalog'

urlpatterns = [
    path('', views.redirect_to_catalog, name='base'),
    path('logout/', views.logout, name='logout'),
    path('', include('django.contrib.auth.urls')),
    path('catalog/', views.show_catalog, name='catalog'),
    path('basket/', views.show_basket, name='basket'),
    path('basket/<int:pk>/delete/', views.delete_item_from_basket, name='delete_from_basket'),
    path('basket/delete/', views.clear_basket, name='clear_basket'),
    path('item/<int:pk>/', views.show_item, name='item'),
    path('item/<int:pk>/add_comment', views.add_comment_to_item, name='add_comment_to_item'),
    path('category/<int:pk>/', views.show_category, name='category'),
    path('reg/', views.RegisterFormView.as_view(), name='registration'),
]
