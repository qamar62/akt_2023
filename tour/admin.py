from django.contrib import admin

# Register your models here.

from .models import *





# class TourGalleryTabularInline(admin.StackedInline):
#     model =  TourGallery
class InclusionTabularInline(admin.StackedInline):
    model =  Inclusions
    extra = 0
class ExclusionTabularInline(admin.StackedInline):
    model =  Excl
    extra = 0
class ItineraryTabularInline(admin.TabularInline):
    model =  Itinerary
    extra = 0
class TourServiceTabularInline(admin.TabularInline):
    model =  TourService
   
    extra = 0

class TourAdmin(admin.ModelAdmin):
    
    model = Tour
    search_fields = ['name']
    list_display = ["name"]
    readonly_fields = ["slug"]
    list_filter = ['name']
    inlines = [InclusionTabularInline, ExclusionTabularInline, ItineraryTabularInline, TourServiceTabularInline]
    date_hierarchy = 'date_created'


admin.site.register(Tour, TourAdmin)
admin.site.register(Promotion)
admin.site.register(Tag)


class ExtraAdmin(admin.ModelAdmin):
    
    model = Extra
    search_fields = ['title']

class PriceAdmin(admin.ModelAdmin):
    
    model = Price
    search_fields = ['tour']
    list_display = ["tour", "adult_price", "child_price", "infant_price"]

admin.site.register(Extra, ExtraAdmin)

admin.site.register(Itinerary)
admin.site.register(Excl)
admin.site.register(Inclusions )
admin.site.register(Category)
admin.site.register(TourGallery)
admin.site.register(Location)
admin.site.register(ReviewRating)
admin.site.register(Price, PriceAdmin)