from django.contrib import admin
from orders.models import *
from django.utils.safestring import mark_safe
from django.urls import reverse


class CustomAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False


class EditLinkToInlineObject(object):
    def extras(self, instance):
        url = reverse('admin:%s_%s_change' % (
            instance._meta.app_label,  instance._meta.model_name),  args=[instance.pk] )
        if instance.pk:
            return mark_safe(u'<a href="{u}">Допы</a>'.format(u=url))
        else:
            return ''


class OrderKurierImageAdmin(admin.ModelAdmin):
    list_display = ['order','image']


class OrderFlowerImageAdmin(admin.ModelAdmin):
    list_display = ['order', 'image']


class Order_items_extra_itemsInline(admin.StackedInline):
    model = Order_items_extra_items
    extra = 0
    readonly_fields = ['extra','amount']

class Order_itemsInline(EditLinkToInlineObject, admin.TabularInline):
    readonly_fields = ['order','item','amount','total_price','extras']
    model = Order_items
    extra = 0


class Order_items_extra_itemsAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}


class Order_itemsAdmin(admin.ModelAdmin):
    readonly_fields = ['order','item','amount','total_price']
    inlines = [Order_items_extra_itemsInline]
    def get_model_perms(self, request):
        return {}


class OrderAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ['id','user', 'first_name', 'status','time' ,'paired','sum_result', 'date_add']
    readonly_fields = ['status','filial','user','archiv','city','like_flower', 'first_name','recipient_phone','adres','date','anonim','sended_phone','email','postcard','comments', 'time' ,'paired','sum_result', 'date_add']
    list_editable = ['status']
    list_filter = [ 'status', 'paired','time', 'date_add']
    date_hierarchy = 'date_add'
    list_max_show_all =10
    inlines = [Order_itemsInline]
    

class FastOrderAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ['first_name', 'flower', 'date_add']
    readonly_fields =  ['first_name', 'city', 'flower', 'date_add','phone']
    list_filter = ['date_add']
    list_max_show_all = 10
    date_hierarchy = 'date_add'


admin.site.register(FasrOrder,FastOrderAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderKurierImage,OrderKurierImageAdmin)
admin.site.register(OrderFlowerImage,OrderFlowerImageAdmin)
admin.site.register(Order_items, Order_itemsAdmin)
admin.site.register(Order_items_extra_items, Order_items_extra_itemsAdmin)
# admin.site.register(CustomAdmin)
# admin.site.register(Order_items_extra_items)
# admin.site.register(Order_items_extra_itemsAdmin)