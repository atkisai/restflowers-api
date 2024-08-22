from rest_framework import serializers
from .models import *

class ContactsSer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = ('__all__')

