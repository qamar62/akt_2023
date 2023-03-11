from django.contrib import admin

# Register your models here.

from .models import *
from django.utils.html import format_html


class TourAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('tour', 'get_month', 'colored_available_dates','colored_unavailable_dates' )

    
    def get_month(self, obj):
        return obj.month
    get_month.short_description = 'Month'
    
    def colored_available_dates(self, obj):
        return format_html('<span style="color: green">{}</span>', obj.available_dates)
    colored_available_dates.short_description = 'Available Dates'

    def colored_unavailable_dates(self, obj):
        return format_html('<span style="color: red">{}</span>', obj.unavailable_dates)
    colored_unavailable_dates.short_description = 'Unavailable Dates'

admin.site.register(TourAvailability, TourAvailabilityAdmin)




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
class TourPriceTabularInline(admin.TabularInline):
    model =  Price
   
    extra = 0

class TourAdmin(admin.ModelAdmin):
    
    model = Tour
    search_fields = ['name']
    list_display = ["name"]
    readonly_fields = ["slug"]
    list_filter = ['name']
    inlines = [InclusionTabularInline, ExclusionTabularInline, ItineraryTabularInline, TourPriceTabularInline]
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
    list_display = ["tour","display_discount","service_type","base_Price", "adult_price", "child_price", "infant_price",'discounted_price']

    def display_discount(self, obj):
        if obj.discount:
            return f"{obj.discount}%"
        else:
            return "-"
    
    display_discount.short_description = "Discount"
    
    def discounted_price(self, obj):
        return obj.get_discounted_price(obj.base_Price)
    
    discounted_price.short_description = "Discounted Price" 
     
            
admin.site.register(Extra, ExtraAdmin)

admin.site.register(Itinerary)
admin.site.register(Excl)
admin.site.register(Inclusions )
admin.site.register(Category)
admin.site.register(TourGallery)
admin.site.register(Location)
admin.site.register(ReviewRating)
admin.site.register(Price, PriceAdmin)