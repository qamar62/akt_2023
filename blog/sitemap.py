from django.contrib.sitemaps import Sitemap

from outbounds.models import Otour
from tour.models import Tour

from . models import Post

class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9
    def items(self):
        return Post.objects.filter(status='published')
    def lastmod(self, obj):
        return obj.post_updated

class OutboundSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9
    def items(self):
        return Otour.objects.filter(available=True)
    def lastmod(self, obj):
        return obj.date_updated

class TourSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9
    def items(self):
        return Tour.objects.filter(available=True)
    def lastmod(self, obj):
        return obj.date_updated