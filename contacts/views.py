from contacts.models import Contacts
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *


@api_view(["POST"])
def GetContacts(request):
    city=request.data.get("city")
    try:
        contact = Contacts.objects.get(city=city)
        contacts = ContactsSer(contacts, many=True).data
        return Response(contacts)
    except:
        contact = None
        return Response("Error")
    
