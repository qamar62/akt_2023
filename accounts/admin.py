from django.contrib import admin

# Register your models here.

from .models import Customer, Contact



admin.site.register(Customer)

admin.site.register(Contact)