from codecs import register
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from . models import *

# Register your models here.

class VisaTypeAdmin(admin.ModelAdmin):
    list_display = ['title','validity', 'multiple_entry', 'active']


admin.site.register(Agent)
admin.site.register(VisaType, VisaTypeAdmin)
admin.site.register(VisaPrice)

@admin.register(Visa)
class VisaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['guest_passport_number']
    list_display = ('agent', "guest_name", "guest_passport_number","guest_gender","guest_nationality", "visa_type", "visa_price", "visa_status")
    list_filter = ['agent']