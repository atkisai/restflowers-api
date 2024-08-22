from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Flowers
class FlowersSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9
    def items(self):
        return Flowers.objects.filter(enable=True)

    def lastmod(self, obj):
        return obj.date_time

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['index', 'allflowers', 'DeliveryView','contacts']

    def location(self, item):
        return reverse(item)
