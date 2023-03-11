from django.contrib import admin
from . models import BookOtour, Obooking, Payment, Booking, BookTour, BookOtour
from import_export.admin import ImportExportModelAdmin
# Register your models here.



class BookTourInline(admin.TabularInline):
    model =  BookTour
    extra = 0
class BookOtourInline(admin.TabularInline):
    model =  BookOtour
    extra = 0



class BookingAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    
    model = Booking
    search_fields = ['first_name']
    list_display = ["created_at","booking_number","first_name",  'payment','country', 'phone', 'email','pickup_location','paymentMode','is_booked', 'qr_tag']
    # readonly_fields = ["slug"]
    list_filter = ['pickup_location', 'paymentMode']
    list_per_page = 20
    inlines = [BookTourInline]
    date_hierarchy = 'created_at'
    
    
    
class ObookingAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    model = Obooking
    search_fields = ['first_name']
    list_display = ["created_at","booking_number","situation","first_name",'country', 'phone', 'email','paymentMode','is_booked','qr_tag']
    # readonly_fields = ["slug"]
    inlines = [BookOtourInline]
    list_per_page = 20
    date_hierarchy = 'created_at'



    


admin.site.register(Payment)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Obooking, ObookingAdmin)

admin.site.register(BookTour)
admin.site.register(BookOtour)