from django.contrib import admin
from django.urls import include, path
from . import views

app_name = 'first_site'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Main.as_view(), name='main'),
    path('home/', include('home.urls'), name='home'),
]
