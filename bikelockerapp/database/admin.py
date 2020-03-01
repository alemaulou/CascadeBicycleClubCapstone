from django.contrib import admin

# Register your models here.
from .models import *

class StationA(admin.ModelAdmin):
    list_display = ('station_name', 'station_county', 'station_zip')
    list_filter = ('station_name', 'station_county', 'station_zip',)


admin.site.register(Station, StationA)
admin.site.register(Locker)
admin.site.register(Maintenance)
admin.site.register(Maintenance_Type)
admin.site.register(Customer)
admin.site.register(Status)
admin.site.register(Cust_Status)
admin.site.register(Cust_Locker)
admin.site.register(Inquiry)
admin.site.register(Inquiry_Loc)
