from django import forms
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from datetime import date, timedelta, datetime
from django.db.models import signals
from django.utils import timezone

class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    location_name = models.CharField('Location Name', max_length=100)
    location_zip = models.CharField('Location Zip', max_length=10)
    location_capacity = models.IntegerField('Location Capacity', default=0)

    def __str__(self):
        return self.location_name

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.pk,))

    def get_location_occ(self):
        return len(Cust_Locker.objects.filter(locker_id__location_id=self.pk))

    def get_renewal_count(self):
        location = Cust_Locker.objects.filter(locker_id__location_id=self.pk)
        if location:
            return len(Cust_Locker.objects.filter(cust_id__status_id__status_name__iexact="Renewed"))
        else:
            return 0

    def get_not_renewed_count(self):
        location = Cust_Locker.objects.filter(locker_id__location_id=self.pk)
        if location:
            return len(Cust_Locker.objects.filter(cust_id__status_id__status_name__iexact="Not Renewing"))
        else:
            return 0

    def get_not_responded(self):
        location = Cust_Locker.objects.filter(locker_id__location_id=self.pk)
        if location:
            print(Cust_Locker.objects.filter(cust_id__status_id__status_name__iexact="Not Responded"))
            return len(Cust_Locker.objects.filter(cust_id__status_id__status_name__iexact="Not Responded"))
        else:
            return 0

    def get_renewal_percentage(self):
        location = Cust_Locker.objects.filter(locker_id__location_id=self.pk)
        if location:
            if (len(Cust_Locker.objects.filter(cust_id__status_id__status_name__iexact="Renewed")) + len(Cust_Locker.objects.filter(cust_id__status_id__status_name__iexact="Not Renewing")) + len(Cust_Locker.objects.filter(cust_id__status_id__status_name__iexact="Not Responded"))) != 0:
                return str(round((len(Cust_Locker.objects.filter(cust_id__status_id__status_name__iexact="Renewed")) + len(Cust_Locker.objects.filter(cust_id__status_id__status_name__iexact="Not Renewing"))) / (len(Cust_Locker.objects.filter(cust_id__status_id__status_name__iexact="Renewed")) + len(Cust_Locker.objects.filter(cust_id__status_id__status_name__iexact="Not Renewing")) + len(Cust_Locker.objects.filter(cust_id__status_id__status_name__iexact="Not Responded"))), 2))
            else:
                return 0
        return 0

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
        return str(self.locker_id) + " #" + self.key_name

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.pk,))

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
    SCOPE = (
        ('General Facility', "General Facility"),
        ('Specific Locker(s)', "Specific Locker(s)"),
    )

    maintenance_id = models.AutoField(primary_key=True)
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    main_type_id = models.ForeignKey(Maintenance_Type, on_delete=models.CASCADE)
    maintenance_scope = models.CharField('Maintenance Scope', choices=SCOPE, max_length=50)
    lockers = models.ManyToManyField(Locker, blank=True)
    maintenance_description = models.CharField('Maintenance Description', max_length=250, default='')
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    main_status_id = models.ForeignKey(Maintenance_Status, on_delete=models.CASCADE, default = 1)

    def __str__(self):
            return str(self.start_date) + " " + self.location_id.location_name + " - " + self.main_type_id.main_type_name
    
    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.pk,))

class Status(models.Model):
    status_id = models.AutoField(primary_key=True)
    status_name = models.CharField('Status Name', max_length=100)
    status_desc = models.CharField('Status Description', max_length=100, blank=True)

    def __str__(self):
        return self.status_name

class Customer(models.Model):
    cust_id = models.AutoField(primary_key=True)
    cust_f_name = models.CharField('First Name', max_length=50)
    cust_l_name = models.CharField('Last Name', max_length=50)
    cust_email = models.EmailField('Email', max_length=100, default='')
    cust_phone = models.CharField('Phone #1', max_length=50, default='')
    cust_phone2 = models.CharField('Phone #2', max_length=50, default='', blank=True)
    cust_address = models.CharField('Street Address', max_length=50, default='')
    cust_city = models.CharField('City', max_length=50)
    cust_state = models.CharField('State', max_length=50)
    cust_zip = models.CharField('Zip Code', max_length=10)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True)
    CONTACTED_ONCE = "Contacted Once"
    CONTACTED_TWICE = "Contacted Twice"
    contacted = models.CharField('Contacted', max_length=50, default='Not Contacted', blank=True)
    # CHOICES = [('option1', 'label 1'), ('option2', 'label 2')]
    # some_field = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())

    def not_responded(self):
        if self.status == Status.objects.get(pk=3):
            return True

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

def delete_inactive_cust_locker(sender, instance, created, **kwargs):
    try:
        cust_locker = Cust_Locker.objects.get(cust_id=instance.cust_id)
        print(cust_locker)
        instance_status = instance.status.status_id
        print(instance_status)
        if instance_status == 4:
            cust_locker.delete()
    except:
        inquiry = None

signals.post_save.connect(receiver=delete_inactive_cust_locker, sender=Customer)

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
    description = models.CharField(max_length=100, default="")

    @property
    def total_lockers(self):
        return Locker.objects.count()

    @property
    def is_past_due(self):
        return date.today() > self.renew_date

    @property
    def is_under_2_weeks_past_due(self):
        if (date.today() > self.renew_date and date.today() - timedelta(14) < self.renew_date) and (self.cust_id.status.status_name == "Not Responded"):
            return True

    @property
    def is_2_weeks_past_due(self):
        return date.today() - timedelta(14) > self.renew_date

    class Meta:
        verbose_name = "Customer Locker"
        verbose_name_plural = "Customer Lockers"

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.pk,))

    def __str__(self):
        return str(self.cust_id) + " " + str(self.locker_id.location_id) + " #" + self.locker_id.locker_name

def create_cust_locker(sender, instance, created, **kwargs):
    try:
        inquiry = Inquiry.objects.get(cust_id=instance.cust_id)
        inquiry.delete()

        # Check to see if locker in use
        locker = Locker.objects.get(locker_id=instance.locker_id.pk)
        locker.locker_status_id = Locker_Status.objects.get(pk=4)
        locker.save()
    except:
        inquiry = None

signals.post_save.connect(receiver=create_cust_locker, sender=Cust_Locker)

class Renewal_Response(models.Model):
    response_id = models.AutoField(primary_key=True)
    response_description = models.CharField('Response Description', max_length=100)

class Locker_Usage(models.Model):
    locker_usage_id = models.AutoField(primary_key=True)
    lu_description = models.CharField('Locker Usage', max_length=100)

class Renewal(models.Model):
    renewal_id = models.AutoField(primary_key=True)
    cust_locker_id = models.ForeignKey(Cust_Locker, on_delete=models.CASCADE)
    sent_date = models.DateField(blank=True)
    response_1 = models.ForeignKey(Renewal_Response, on_delete=models.CASCADE, related_name='response1', blank=True)
    sent_date_2 = models.DateField(blank=True)
    response_2 = models.ForeignKey(Renewal_Response, on_delete=models.CASCADE, related_name='response2', blank=True)
    phone_call_date = models.DateField('Phone Call Date', default=timezone.now(), blank=True)
    response_3 = models.ForeignKey(Renewal_Response, on_delete=models.CASCADE, related_name='response3', blank=True)

class Inquiry(models.Model):
    inquiry_id = models.AutoField(primary_key=True)
    cust_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    inquiry_date = models.DateField()
    locations = models.ManyToManyField(Location)

    @property
    def is_empty(self):
        if Inquiry.objects.count() == 0:
            return True

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

class Staff(models.Model):
    staff_id = models.AutoField(primary_key=True)
    staff_f_name = models.CharField('First Name', max_length=50)
    staff_l_name = models.CharField('Last Name', max_length=50)
    staff_email = models.EmailField('Email', max_length=100, default='')
    staff_phone = models.CharField('Phone #1', max_length=50, default='')
    staff_phone2 = models.CharField('Phone #2', max_length=50, default='', blank=True)
    staff_address = models.CharField('Street Address', max_length=50, default='')
    staff_city = models.CharField('City', max_length=50)
    staff_state = models.CharField('State', max_length=50)
    staff_zip = models.CharField('Zip Code', max_length=10)

    def phone_number(self):
        if self.staff_phone:
            first = self.staff_phone[0:3]
            second = self.staff_phone[3:6]
            third = self.staff_phone[6:10]
            return '(' + first + ')' + ' ' + second + '-' + third
        else:
            return 'N/A'

    def phone_number2(self):
        if self.staff_phone2:
            first = self.staff_phone2[0:3]
            second = self.staff_phone2[3:6]
            third = self.staff_phone2[6:10]
            return '(' + first + ')' + ' ' + second + '-' + third
        else:
            return 'N/A'

    def __str__(self):
        return self.staff_f_name + " " + self.staff_l_name

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.pk,))

    class Meta:
        ordering = ['staff_l_name']

class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Locker_Log(TimeStamp):
    locker_log_id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    cust_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    action = models.CharField('Action', max_length=500, blank=True)
    action_done = models.CharField('Action Done', max_length=500, blank=True)
    next_step = models.CharField('Action', max_length=500, blank=True)
    resolved = models.BooleanField('Resolved', default=False)

    class Meta:
        verbose_name = "Locker Log"
        verbose_name_plural = "Locker Logs"



