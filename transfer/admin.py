from django.contrib import admin

# Register your models here.
from . models import *
from import_export.admin import ImportExportModelAdmin



class PriceTabularInline(admin.TabularInline):
    model =  Price
    extra = 0

class TransferAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    
    model = Transfer
    search_fields = ['name']
    
    readonly_fields = ["slug"]
    list_filter = ['name']
    inlines = [PriceTabularInline]
    date_hierarchy = 'date_created'
    


admin.site.register(Transfer, TransferAdmin)
admin.site.register(PickupLocation)
admin.site.register(DropoffLocation)
