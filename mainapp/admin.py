from django.contrib import admin
from mainapp.models import *


class ImagesAdmin(admin.StackedInline):
    model = FlowerImages
    extra = 0

class FlowerAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'price', 'count_in', 'enable', 'ready', 'get_cities', 'filial']
    list_editable = ['price', 'count_in', 'enable', 'ready']
    list_filter = ['enable', 'filial', 'ready', 'category', 'city', 'povod','comp', 'valentine', 'stock', 'date_time']
    search_fields = ['name', 'description']
    exclude = ['col','total']
    date_hierarchy = 'date_time'
    inlines = [ImagesAdmin]
    list_max_show_all = 10
    def get_cities(self, obj):  
        return "\n".join([p.name for p in obj.city.all()])
    get_cities.short_description = 'Город'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


class PovodsAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


class UsersAdmin(admin.ModelAdmin):
    list_display = ['user', 'work', 'city', 'filial']
    list_filter = ['work']
    list_editable = ['work', 'city', 'filial']
    def get_form(self, request, obj=None, **kwargs):
        #убирает возможность редактировать/удалять города и связанные данные
        form = super(UsersAdmin, self).get_form(request, obj, **kwargs)
        field = form.base_fields["city"]
        field.widget.can_add_related = False
        field.widget.can_change_related = False
        field.widget.can_delete_related = False
        return form

class CityAdmin(admin.ModelAdmin):
    list_display = ['name']
    readonly_fields = ('id',)   
    search_fields = ['name']


class TextContentAdmin(admin.ModelAdmin):
    list_display = ['title']


class FilialAdmin(admin.ModelAdmin):
    list_display = ['name']

class ExtraProductsAdmin(admin.ModelAdmin):
    exclude = ['col','selected','total']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Povods, PovodsAdmin)
admin.site.register(Flowers, FlowerAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Counts_Flowers)
admin.site.register(Users, UsersAdmin)
admin.site.register(ExtraProducts, ExtraProductsAdmin)
# admin.site.register(TextDescription)
# admin.site.register(TextContent, TextContentAdmin)
# admin.site.register(Delivery)
admin.site.register(Filial, FilialAdmin)
admin.site.register(FlowerImages)
admin.site.register(SetsExtraProducts)
