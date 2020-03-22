from django.contrib import admin

# Register your models here.
from .models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class LocationA(admin.ModelAdmin):
    list_display = ('location_name', 'location_zip')
    list_filter = ('location_name', 'location_zip',)

class CustomerResource(resources.ModelResource):
    class Meta:
        model = Customer

class CustomerAdmin(ImportExportModelAdmin):
    resource_class = CustomerResource


admin.site.register(Location, LocationA)
admin.site.register(Locker)
admin.site.register(Maintenance)
admin.site.register(Maintenance_Type)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Status)
admin.site.register(Cust_Status)
admin.site.register(Cust_Locker)
admin.site.register(Inquiry)
