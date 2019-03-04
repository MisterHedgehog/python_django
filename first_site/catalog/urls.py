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
    #path('basket/add', views.show_item, name='add_item_in_basket'),
    path('pre_deal/', views.show_deal, name='confirm_deal'),
    path('deal/', views.make_deal, name='make_deal'),
    path('item/<int:pk>/', views.show_item, name='item'),
    path('item/<int:pk>/add_comment', views.add_comment_to_item, name='add_comment_to_item'),
    path('item/select/add', views.select_category_before_add_item, name='select_category_before_add'),
    path('item/<int:category>/add', views.add_item_to_database, name='add_item_to_database'),
    path('category/<int:category_id>/', views.show_category, name='category'),
    path('reg/', views.RegisterFormView.as_view(), name='registration'),
    path('profile', views.show_profile, name='profile')
]
