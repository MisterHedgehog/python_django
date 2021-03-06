from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

app_name = 'first_site'

urlpatterns = [
    path('', include('catalog.urls'), name='base'),
    path('admin/', admin.site.urls),
    ]

# Необходимо для использования медиа-контента
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
