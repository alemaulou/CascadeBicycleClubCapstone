from django.db import models

# Create your models here.
from django.db import models

class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    location_name = models.CharField('Location Name', max_length=100)
    location_zip = models.CharField('Location Zip', max_length=10)

    def __str__(self):
        return self.location_name

class Locker_Status(models.Model):
    locker_status_id = models.AutoField(primary_key=True)
    locker_status_name = models.CharField('Locker Status Name', max_length=100)
    
    def __str__(self):
        return self.locker_status_name
    
    class Meta:
        verbose_name = "Locker Status"
        verbose_name_plural = "Locker Statuses"

class Locker(models.Model):
    locker_id = models.AutoField(primary_key=True)
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    locker_name = models.CharField('Locker Name', max_length=100)
    locker_status_id = models.ForeignKey(Locker_Status, on_delete=models.CASCADE, default=1)
    def __str__(self):
        return self.location_id.location_name + " #" + self.locker_name

class Key_Status(models.Model):
    key_status_id = models.AutoField(primary_key=True)
    key_status_name = models.CharField('Key Status Name', max_length=100)

    def __str__(self):
        return self.key_status_name
    
    class Meta:
        verbose_name = "Key Status"
        verbose_name_plural = "Key Statuses"
    
class Key(models.Model):
    key_id = models.AutoField(primary_key=True)
    locker_id = models.ForeignKey(Locker, on_delete=models.CASCADE)
    key_name = models.CharField('Key Name', max_length=100)
    key_status_id = models.ForeignKey(Key_Status, on_delete=models.CASCADE, default = 1)
    def __str__(self):
        return self.locker_id.locker_name + " #" + self.key_name


class Maintenance_Type(models.Model):
    main_type_id = models.AutoField('Maintenance Type',primary_key=True)
    main_type_name = models.CharField('Maintenance Type Name', max_length=100)
    main_type_desc = models.CharField('Maintenance Type Description', max_length=100)

    class Meta:
        verbose_name = "Maintenance Type"
        verbose_name_plural = "Maintenance Types"
    
    def __str__(self):
        return self.main_type_name
    def __unicode__(self):
        return self.main_type_name

class Maintenance_Status(models.Model):
    main_status_id = models.AutoField(primary_key=True)
    main_status_name = models.CharField('Maintenance Status Name', max_length=100)

    def __str__(self):
        return self.main_status_name

    class Meta:
        verbose_name = "Maintenance Status"
        verbose_name_plural = "Maintenance Statuses"

class Maintenance(models.Model):
    SCOPE_CHOICES = (
        ('general facility', "General Facility"),
        ('specific locker(s)', "Specific Locker(s)"),
    )

    maintenance_id = models.AutoField(primary_key=True)
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    main_type_id = models.ForeignKey(Maintenance_Type, on_delete=models.CASCADE)
    maintenance_scope = models.CharField('Maintenance Scope', choices=SCOPE_CHOICES, max_length=50)
    lockers = models.ManyToManyField(Locker, blank=True)
    maintenance_description = models.CharField('Maintenance Description', max_length=250, default='')
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    main_status_id = models.ForeignKey(Maintenance_Status, on_delete=models.CASCADE, default = 1)

    def __str__(self):
            return str(self.start_date) + " " + self.location_id.location_name + " - " + self.main_type_id.main_type_name

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

class Cust_Locker(models.Model):
    cust_lock_id = models.AutoField(primary_key=True)
    cust_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    locker_id = models.ForeignKey(Locker, on_delete=models.CASCADE)
    contract_date = models.DateField()
    renew_date = models.DateField()

    class Meta:
        verbose_name = "Customer Locker"
        verbose_name_plural = "Customer Lockers"

class Inquiry(models.Model):
    inquiry_id = models.AutoField(primary_key=True)
    cust_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    inquiry_date = models.DateField()
    locations = models.ManyToManyField(Location)

    class Meta:
        verbose_name = "Inquiry"
        verbose_name_plural = "Inquiries"