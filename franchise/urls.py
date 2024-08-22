from django.urls import path
from franchise import views


urlpatterns = [
    path('', views.Franchise, name='index'),
]