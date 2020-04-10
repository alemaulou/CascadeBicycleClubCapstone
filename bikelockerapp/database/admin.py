from django.contrib import admin

# Register your models here.
from .models import *

class LocationA(admin.ModelAdmin):
    list_display = ('location_name', 'location_zip')
    list_filter = ('location_name', 'location_zip',)
    def update_status(self, request, queryset):
        queryset.update(status='NEW_STATUS')

    update_status.short_description = "Update status    "

admin.site.register(Location, LocationA)
admin.site.register(Waitlist)
admin.site.register(Locker_Status)
admin.site.register(Locker)
admin.site.register(Key_Status)
admin.site.register(Key)
admin.site.register(Maintenance_Type)
admin.site.register(Customer)
admin.site.register(Status)
admin.site.register(Cust_Status)
admin.site.register(Maintenance_Status)
admin.site.register(Maintenance)
admin.site.register(Cust_Locker)
admin.site.register(Inquiry)