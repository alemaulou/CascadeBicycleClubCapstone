from django.db import models

# Create your models here.
from django.db import models

class Station(models.Model):
    station_id = models.AutoField(primary_key=True)
    station_name = models.CharField('Station Name', max_length=100)
    station_county = models.CharField('Station County', max_length=50)
    station_zip = models.CharField('Station Zip', max_length=10)

    def __str__(self):
        return self.station_name

    def show_county(self):
        return self.station_county

class Locker(models.Model):
    locker_id = models.AutoField(primary_key=True)
    station_id = models.ForeignKey(Station, on_delete=models.CASCADE)
    locker_name = models.CharField('Locker Name', max_length=100)

class Maintenance_Type(models.Model):
    main_type_id = models.AutoField(primary_key=True)
    main_type_name = models.CharField('Maintenance Type Name', max_length=100)
    main_type_desc = models.CharField('Maintenance Type Description', max_length=100)
 
class Maintenance(models.Model):
    maintenance_id = models.AutoField(primary_key=True)
    locker_id = models.ForeignKey(Locker, on_delete=models.CASCADE)
    main_type_id = models.ForeignKey(Maintenance_Type, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

class Customer(models.Model):
    cust_id = models.AutoField(primary_key=True)
    cust_f_name = models.CharField('First Name', max_length=50)
    cust_l_name = models.CharField('Last Name', max_length=50)
    cust_email = models.EmailField('Email', max_length=100, default='')
    cust_address = models.CharField('Street Address', max_length=50, default='')
    cust_city = models.CharField('City', max_length=50)
    cust_state = models.CharField('State', max_length=50)
    cust_zip = models.CharField('Zip Code', max_length=10)

class Status(models.Model):
    status_id = models.AutoField(primary_key=True)
    status_name = models.CharField('Status Name', max_length=100)
    status_desc = models.CharField('Status Description', max_length=100)
 
 
class Cust_Status(models.Model):
    cust_status_id = models.AutoField(primary_key=True)
    cust_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status_id = models.ForeignKey(Status, on_delete=models.CASCADE)
    cust_status_date = models.DateField()
 

class Cust_Locker(models.Model):
    cust_lock_id = models.AutoField(primary_key=True)
    cust_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    locker_id = models.ForeignKey(Locker, on_delete=models.CASCADE)
    contract_date = models.DateField()
    renew_date = models.DateField()

class Inquiry(models.Model):
    inquiry_id = models.AutoField(primary_key=True)
    cust_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    inquiry_date = models.DateField()
 
class Inquiry_Loc(models.Model):
    inquiry_loc_id = models.AutoField(primary_key=True)
    inquiry_id = models.ForeignKey(Inquiry, on_delete=models.CASCADE)
    station_id = models.ForeignKey(Station, on_delete=models.CASCADE)