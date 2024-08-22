from django.contrib import admin
from django.db import models
from franchise.models import Order

class OrderAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ['fio', 'phone', 'city_fr', 'brend', 'date_add']
    # readonly_fields =  ['fio', 'city', 'phone', 'date_add']

admin.site.register(Order, OrderAdmin)
