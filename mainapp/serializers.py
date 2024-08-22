from dataclasses import fields
from unicodedata import category
from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class CategorySer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('__all__')


class PovodsSer(serializers.ModelSerializer):
    class Meta:
        model = Povods
        fields = ('__all__')


# class TextDescriptionSer(serializers.ModelSerializer):
#     class Meta:
#         model = TextDescription
#         fields = ('__all__')


# class TextNameSer(serializers.ModelSerializer):
#     class Meta:
#         model = TextName
#         fields = ('__all__')


class FlowerImagesSer(serializers.ModelSerializer):
    class Meta:
        model = FlowerImages
        fields = ['image','id']


class ExtraProductsSer(serializers.ModelSerializer):
    class Meta:
        model = ExtraProducts
        fields = ('__all__')


class SetsExtraProductsSer(serializers.ModelSerializer):
    extra = ExtraProductsSer(many=True)
    class Meta:
        model = SetsExtraProducts
        fields = ('__all__')


class FlowersSer(serializers.ModelSerializer):
    images = FlowerImagesSer(many=True)
    category = CategorySer(many=True)
    povod = PovodsSer(many=True)
    set = SetsExtraProductsSer(many=False)
    class Meta:
        model = Flowers
        fields = ('__all__')


class CitySer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('__all__')


