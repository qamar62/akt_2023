from django.contrib import admin

# Register your models here.

from .models import *
from import_export.admin import ImportExportModelAdmin





class TourGalleryTabularInline(admin.TabularInline):
     model =  OtourGallery
class InclusionTabularInline(admin.TabularInline):
    model =  Inclusions
    extra = 0
class ExclusionTabularInline(admin.TabularInline):
    model =  Exclusions
    extra = 0
class ItineraryTabularInline(admin.TabularInline):
    model =  Itinerary
    extra = 0
class TourOptions(admin.TabularInline):
    model =  Optional
    extra = 0
class TourPrice(admin.TabularInline):
    model =  Price
    extra = 0
   
class ItineraryAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    model = Itinerary
    
    list_display = ["tour",  'title', 'time', 'detail']
    
    
class ExclusionAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    model = Exclusions
    
    list_display = ["tour",  'name']
class InclusionAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    model = Inclusions
    
    list_display = ["tour",  'name']
    
    
   
    
    
class TourAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    
    model = Otour
    search_fields = ['name']
    list_display = ["name",  'no_of_days', 'no_of_nights', 'seats']
    readonly_fields = ["slug"]
    list_filter = ['name']
    inlines = [InclusionTabularInline, ExclusionTabularInline, ItineraryTabularInline, TourOptions, TourPrice]
    date_hierarchy = 'date_created'
    


admin.site.register(Otour, TourAdmin)
admin.site.register(Offer)
admin.site.register(Tag)

admin.site.register(Itinerary, ItineraryAdmin)
admin.site.register(Exclusions, ExclusionAdmin)
admin.site.register(Inclusions, InclusionAdmin )
admin.site.register(Category)
admin.site.register(OtourGallery)
admin.site.register(Location)
admin.site.register(Inquiry)




