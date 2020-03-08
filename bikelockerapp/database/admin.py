from django.contrib import admin

# Register your models here.
from .models import *

class LocationA(admin.ModelAdmin):
    list_display = ('location_name', 'location_zip')
    list_filter = ('location_name', 'location_zip',)


admin.site.register(Location, LocationA)
admin.site.register(Locker)
admin.site.register(Maintenance)
admin.site.register(Maintenance_Type)
admin.site.register(Customer)
admin.site.register(Status)
admin.site.register(Cust_Status)
admin.site.register(Cust_Locker)
admin.site.register(Inquiry)
