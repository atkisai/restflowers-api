from rest_framework import serializers
from .models import *
from mainapp.serializers import FlowersSer, CitySer, ExtraProductsSer


class Order_items_extra_itemsSer(serializers.ModelSerializer):
    extra = ExtraProductsSer(many=False)
    class Meta:
        model = Order_items_extra_items
        fields = ('__all__')


class OrderItemsSer(serializers.ModelSerializer):
    item = FlowersSer(many=False)
    extra_item = Order_items_extra_itemsSer(many=True)
    class Meta:
        model = Order_items
        fields = ('__all__')


class OrdersSer(serializers.ModelSerializer):
    order_items = OrderItemsSer(many=True)
    city = CitySer(many=False)
    class Meta:
        model = Order
        fields = ('__all__')


