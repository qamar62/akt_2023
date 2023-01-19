from django.contrib import admin
from tour.models import TourService
from  . models import Newsletter, Faq, FaqServices, HappyCutomer
# Register your models here.


admin.site.register(TourService)
admin.site.register(Newsletter)
admin.site.register(FaqServices)
admin.site.register(Faq)
admin.site.register(HappyCutomer)