from django.contrib import admin
from contacts.models import Contacts


# class ContactsAdmin(GetQueryByCityMixin, admin.ModelAdmin):
#     list_display = ['city']
admin.site.register(Contacts)

