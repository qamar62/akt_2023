from django.contrib import admin

# Register your models here.
from . models import *


admin.site.register(Transfer)
admin.site.register(PickupLocation)
admin.site.register(DropoffLocation)
