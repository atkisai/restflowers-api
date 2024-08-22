from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf.urls.static import static
from royalflowers import settings

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/',include('mainapp.urls')),
    path('api/franchise/',include('franchise.urls')),
    path('api/contacts/',include('contacts.urls')),
    path('api/order/',include('orders.urls')),
]\
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
              + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
