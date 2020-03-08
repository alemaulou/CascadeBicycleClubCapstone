from django.db import models

# Create your models here.
from django.db import models

class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    location_name = models.CharField('Location Name', max_length=100)
    location_zip = models.CharField('Location Zip', max_length=10)

    def __str__(self):
        return self.location_name

class Locker(models.Model):
    locker_id = models.AutoField(primary_key=True)
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
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

    def __str__(self):
        return self.cust_f_name + " " + self.cust_l_name

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
    locations = models.ManyToManyField(Location)