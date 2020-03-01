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

class Loc_Maintenance(models.Model):
    loc_main_id = models.AutoField(primary_key=True)
    locker_id = models.ForeignKey(Locker, on_delete=models.CASCADE)

class Maintenance_Type(models.Model):
    main_type_id = models.AutoField(primary_key=True)
    main_type_name = models.CharField('Maintenance Type Name', max_length=100)
    main_type_desc = models.CharField('Maintenance Type Description=', max_length=100)

class Maintenance(models.Model):
    main_id = models.AutoField(primary_key=True)
    main_type_id = models.ForeignKey(Maintenance_Type, on_delete=models.CASCADE)
    main_start_date = models.DateField()
    main_end_date = models.DateField()

class Customer(models.Model):
    cust_id = models.AutoField(primary_key=True)
    cust_f_name = models.CharField('First Name', max_length=50)
    cust_l_name = models.CharField('Last Name', max_length=50)
    cust_email = models.EmailField('Email', max_length=100, default='')
    cust_address = models.CharField('Street Address', max_length=50, default='')
    cust_city = models.CharField('City', max_length=50)
    cust_state = models.CharField('State', max_length=50)
    cust_zip = models.CharField('Zip Code', max_length=10)

class Cust_Status_Type(models.Model):
    cust_stat_type_id = models.AutoField(primary_key=True)
    cust_stat_type_name = models.CharField('Customer Status Type Name', max_length=100)
    cust_stat_type_desc = models.CharField('Customer Status Type description', max_length=100)


class Cust_Status(models.Model):
    cust_status_id = models.AutoField(primary_key=True)
    cust_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    cust_status_type_id = models.ForeignKey(Cust_Status_Type, on_delete=models.CASCADE)
    station_id = models.ForeignKey(Station, on_delete=models.CASCADE)
    cust_status_date = models.DateField()

class Cust_Loc(models.Model):
    cust_loc_id = models.AutoField(primary_key=True)
    cust_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    locker_id = models.ForeignKey(Locker, on_delete=models.CASCADE)
    contract_date = models.DateField()
    renew_date = models.DateField()

class Event_Type(models.Model):
    event_type_id = models.AutoField(primary_key=True)
    event_type_name = models.CharField('Event Type Name', max_length=100)
    event_type_desc = models.CharField('Event Type Description', max_length=200)

class Event_Status(models.Model):
    event_status_id = models.AutoField(primary_key=True)
    event_status_name = models.CharField('Event Status Name', max_length=100)
    event_status_desc = models.CharField('Event Status Description', max_length=200)

class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    event_type_id = models.ForeignKey(Event_Type, on_delete=models.CASCADE)
    event_status_id = models.ForeignKey(Event_Status, on_delete=models.CASCADE)
    event_name = models.CharField('Event Name', max_length=100)
    event_start_date = models.DateField()
    event_end_date = models.DateField()

class Cust_Loc_Event(models.Model):
    cust_loc_event_id = models.AutoField(primary_key=True)
    cust_loc_id = models.ForeignKey(Cust_Loc, on_delete=models.CASCADE)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
