from django.db import models
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from datetime import date

class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    location_name = models.CharField('Location Name', max_length=100)
    location_zip = models.CharField('Location Zip', max_length=10)

    def __str__(self):
        return self.location_name

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.pk,))

class Locker(models.Model):
    locker_id = models.AutoField(primary_key=True)
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    locker_name = models.CharField('Locker Name', max_length=100)

    def __str__(self):
        return str(self.location_id) + " #" + self.locker_name

class Maintenance_Type(models.Model):
    main_type_id = models.AutoField(primary_key=True)
    main_type_name = models.CharField('Maintenance Type Name', max_length=100)
    main_type_desc = models.CharField('Maintenance Type Description', max_length=100)

    class Meta:
        verbose_name = "Maintenance Type"
        verbose_name_plural = "Maintenance Types"

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
    cust_phone = models.CharField('Phone #1', max_length=50, default='')
    cust_phone2 = models.CharField('Phone #2', max_length=50, default='')
    cust_address = models.CharField('Street Address', max_length=50, default='')
    cust_city = models.CharField('City', max_length=50)
    cust_state = models.CharField('State', max_length=50)
    cust_zip = models.CharField('Zip Code', max_length=10)

    def phone_number(self):
        if self.cust_phone:
            first = self.cust_phone[0:3]
            second = self.cust_phone[3:6]
            third = self.cust_phone[6:10]
            return '(' + first + ')' + ' ' + second + '-' + third
        else:
            return 'N/A'

    def phone_number2(self):
        if self.cust_phone2:
            first = self.cust_phone2[0:3]
            second = self.cust_phone2[3:6]
            third = self.cust_phone2[6:10]
            return '(' + first + ')' + ' ' + second + '-' + third
        else:
            return 'N/A'

    def __str__(self):
        return self.cust_f_name + " " + self.cust_l_name

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.pk,))

    class Meta:
        ordering = ['cust_l_name']

class Status(models.Model):
    status_id = models.AutoField(primary_key=True)
    status_name = models.CharField('Status Name', max_length=100)
    status_desc = models.CharField('Status Description', max_length=100)
 
 
class Cust_Status(models.Model):
    cust_status_id = models.AutoField(primary_key=True)
    cust_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status_id = models.ForeignKey(Status, on_delete=models.CASCADE)
    cust_status_date = models.DateField()

    class Meta:
        verbose_name = "Customer Status"
        verbose_name_plural = "Customer Statuses"

class Cust_Locker(models.Model):
    cust_lock_id = models.AutoField(primary_key=True)
    cust_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    locker_id = models.ForeignKey(Locker, on_delete=models.CASCADE)
    contract_date = models.DateField()
    renew_date = models.DateField()

    @property
    def is_past_due(self):
        return date.today() > self.renew_date

    def is_renew(self):
        return date.today()-30 > self.renew_date

    def contains(self, item):
        if Cust_Locker.filter(cust_id=item.id).exists():
            return True

    class Meta:
        verbose_name = "Customer Locker"
        verbose_name_plural = "Customer Lockers"

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.pk,))

    def __str__(self):
        return str(self.cust_id) + " " + str(self.locker_id.location_id) + " #" + self.locker_id.locker_name

class Inquiry(models.Model):
    inquiry_id = models.AutoField(primary_key=True)
    cust_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    inquiry_date = models.DateField()
    locations = models.ManyToManyField(Location)

    class Meta:
        verbose_name = "Inquiry"
        verbose_name_plural = "Inquiries"

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.pk,))

    def __str__(self):
        return str(self.cust_id) + " (" + str(self.inquiry_date) + ")"

class Waitlist(models.Model):
    waitlist_id = models.AutoField(primary_key=True)
    cust_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    waitlist_date = models.DateField()
    locations = models.ManyToManyField(Location)

    class Meta:
        verbose_name = "Waitlist"
        verbose_name_plural = "Waitlists"

    def __str__(self):
        return str(self.cust_id)