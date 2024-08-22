from mainapp.models import *
from datetime import date


def my_scheduled_job():
    today = date.today()
    flowers = Flowers.objects.all()
    for flower in flowers:
        if flower.end_stock == today:
            flower.stock=False
            flower.start_stock=None
            flower.end_stock=None
            flower.save()