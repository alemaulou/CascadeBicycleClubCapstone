import csv, io

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, BadHeaderError, HttpResponse
from django.contrib import messages
from .models import Customer, Inquiry, Location, Cust_Locker, Maintenance, Locker, Waitlist, Locker_Log, Status
from .forms import CustomerForm, SendEmailForm, SendEmailFormAfter2Weeks
from datetime import datetime, date, timedelta
from django.conf import settings
from django.core.paginator import Paginator

@staff_member_required
# Admin Index View
def index(request):

    # Querying for data to display on main page
    all_inquiry = Inquiry.objects.all()
    all_station = Location.objects.all()
    all_customer = Customer.objects.all()
    all_cust_locker = Cust_Locker.objects.all()
    all_maintenance = Maintenance.objects.all()

    # Checking to see if user input in search field "contains" query
    location_contains_query = request.GET.get('location')
    customer_contains_query = request.GET.get('customer')

    # Filtering customer data (station, locker, inquiry) by location
    if location_contains_query != '' and location_contains_query is not None:
        all_cust_locker = all_cust_locker.filter(locker_id__location_id__location_name__contains=location_contains_query)
        all_inquiry = all_inquiry.filter(locations__location_name__contains=location_contains_query)
        all_maintenance = all_maintenance.filter(lockers__location_id__location_name__contains=location_contains_query)

    # Filtering customer data by customer name
    if customer_contains_query != '' and customer_contains_query is not None:
        customers = []
        if all_cust_locker.filter(cust_id__cust_f_name__icontains=customer_contains_query) | all_cust_locker.filter(cust_id__cust_l_name__icontains=customer_contains_query):
            customers += all_cust_locker.filter(cust_id__cust_f_name__icontains=customer_contains_query)
            customers += all_cust_locker.filter(cust_id__cust_l_name__icontains=customer_contains_query)
        all_cust_locker = customers
        all_inquiry = all_inquiry.filter(cust_id__cust_f_name__contains=customer_contains_query)

    # Rendering boolean for Locker Renewals
    contains_locker_renewals = False
    for locker_renewals in all_cust_locker:
        if date.today() > locker_renewals.renew_date:
            contains_locker_renewals = True

    # Returning values to to render onto template
    render_dicts = {'all_stations': all_station, 'all_customer': all_customer, 'all_inquiries': all_inquiry, 'all_cust_lockers': all_cust_locker, 'locker_renewals': contains_locker_renewals, 'all_maintenance' : all_maintenance}
    return render(request, 'admin/index.html', render_dicts)

def BootstrapFilterView(request):
    render(request, "bootstrap_form.html ")

@staff_member_required
# Customer Upload Data View
def customer_upload(request):
    # Import data template
    template = "customer_upload.html"

    prompt = {
        'order': 'Order of CSV should be the following: cust_f_name, cust_l_name, cust_email, address, city, state, zip'
    }

    if request.method == "GET":
        return render(request, template, prompt)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'This is not a CSV file')

    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)

    # Scraping data from CSV file.
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, created = Customer.objects.update_or_create(
            cust_f_name = column[0],
            cust_l_name = column[1],
            cust_email = column[6],
            cust_address = column[2],
            cust_city = column[3],
            cust_state = column[4],
            cust_zip = column[5]
        )

    context = {}
    return render(request, template, context)

@staff_member_required
# Customer Waitlist View
def customer_waitlist(request):
    submitted = False
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            identity = customer.pk
            locs = form.cleaned_data['locations']
            obj = Customer.objects.get(cust_id=identity)
            waitlist = Waitlist.objects.create(
                cust_id = Customer.objects.get(cust_id = obj.pk),
                waitlist_date = datetime.now())
            waitlist.locations.add(*locs)
            return HttpResponseRedirect('/customer_inquiry/?submitted=True')
    else:
        form = CustomerForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'customer_inquiry.html', {'form': form, 'submitted': submitted})

# Admin E-Mail Renewals View
@staff_member_required
def send_email(request):
    x = [obj.cust_id.cust_email for obj in Cust_Locker.objects.all() if obj.is_under_2_weeks_past_due]
    y = [obj.cust_id.cust_email for obj in Cust_Locker.objects.all() if obj.is_2_weeks_past_due]
    all_stations = Location.objects.all()
    all_cust_locker = Cust_Locker.objects.all()
    if request.method == 'GET':
        form = SendEmailForm()
        form2 = SendEmailFormAfter2Weeks()
    if request.method == 'POST' and 'form1' in request.POST:
        form = SendEmailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            from_email = settings.EMAIL_HOST_USER
            try:
                send_mail(subject, message, from_email, x, fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('thanks')
    if request.method == 'POST' and 'form2' in request.POST:
        form2 = SendEmailFormAfter2Weeks(request.POST)
        if form2.is_valid():
            subject = form2.cleaned_data['subject']
            print(subject)
            message = form2.cleaned_data['message']
            print(message)
            from_email = settings.EMAIL_HOST_USER
            try:
                send_mail(subject, message, from_email, y, fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('thanks')

    # Rendering boolean for Locker Renewals
    contains_locker_renewals = False
    for locker_renewals in all_cust_locker:
        if date.today() > locker_renewals.renew_date:
            contains_locker_renewals = True

    # Rendering boolean for New Locker Renewal Requests
    contains_lr_under_2_weeks = False
    for locker_renewals in all_cust_locker:
        if date.today() > locker_renewals.renew_date and date.today() - timedelta(14) < locker_renewals.renew_date:
            contains_lr_under_2_weeks = True

    # Rendering boolean for Past due (over 2 week) Locker Renewal Requests
    contains_lr_over_2_weeks = False
    for locker_renewals in all_cust_locker:
        if date.today() - timedelta(14) > locker_renewals.renew_date:
            contains_lr_over_2_weeks = True

    # Total number of Lockers by Location Capacity
    total_lockers = 0
    for location in all_stations:
        total_lockers += location.location_capacity

    # Total number of Occupied Lockers
    total_occupied = len(all_cust_locker)

    return render(request, 'send_email.html',
                  {'all_stations': all_stations,
                   'form': form,
                   'form2': form2,
                   'emails': x,
                   '2_weeks': y,
                   'all_cust_lockers': all_cust_locker,
                   'locker_renewals': contains_locker_renewals,
                   'lr_over_2': contains_lr_over_2_weeks,
                   'lr_under_2': contains_lr_under_2_weeks,
                   'total_lockers': total_lockers,
                   'total_occupied': total_occupied})

@staff_member_required
def renewals(request):
    # Querying for data.
    all_stations = Location.objects.all()
    all_cust_locker = Cust_Locker.objects.filter(cust_id__status_id__status_name__iexact="Not Responded")
    paginator = Paginator(all_cust_locker, 1)
    page = request.GET.get('page')
    # Total number of Lockers by Location Capacity
    total_lockers = 0
    for location in all_stations:
        total_lockers += location.location_capacity

    # Total number of Occupied Lockers
    total_occupied = len(all_cust_locker)

    ## Get Total Customer Renewal Status to render
    # Total Renewing
    locker_renewal_count_total = 0
    for locker in all_stations:
        if Cust_Locker.objects.filter(locker_id__location_id=locker.pk) and Cust_Locker.objects.filter(cust_id__status_id__status_name__iexact="Renewed"):
            locker_renewal_count_total += 1

    # Not Renewing
    locker_not_renewal_count_total = 0
    for locker in all_stations:
        if Cust_Locker.objects.filter(locker_id__location_id=locker.pk) and Cust_Locker.objects.filter(cust_id__status_id__status_name__iexact="Not Renewing"):
            locker_not_renewal_count_total += 1

    # Not Responded
    not_responded_count_total = 0
    for locker in all_stations:
        if Cust_Locker.objects.filter(locker_id__location_id=locker.pk) and Cust_Locker.objects.filter(cust_id__status_id__status_name__iexact="Not Responded"):
            not_responded_count_total += 1

    # Calculation for number responded and total
    total_percentage_responded = 0
    if (locker_renewal_count_total + locker_not_renewal_count_total + not_responded_count_total) != 0:
        total_percentage_responded = (locker_renewal_count_total + locker_not_renewal_count_total) / (locker_renewal_count_total + locker_not_renewal_count_total + not_responded_count_total)
        print(total_percentage_responded)
    else:
        total_percentage_responded = 0

    # Selecting which buttons pressed and querying Customer
    list_of_id_for_action = request.POST.getlist('for_action')
    list_of_id_for_action2 = request.POST.getlist('for_action2')
    list_of_obj = Customer.objects.filter(cust_id__in=list_of_id_for_action)
    list_of_obj_not_renewing = Customer.objects.filter(cust_id__in=list_of_id_for_action2)
    renewing_status = Status.objects.get(pk=1)
    not_renewing_status = Status.objects.get(pk=2)
    not_responded_status = Status.objects.get(pk=3)
    if 'save' in request.POST:
        if list_of_obj:
            list_of_obj.update(status=renewing_status)
        if list_of_obj_not_renewing:
            list_of_obj_not_renewing.update(status=not_renewing_status)
        return HttpResponseRedirect("renewals")

    # Mass update
    if 'list' in request.POST:
        active_customers = Customer.objects.all().exclude(status_id__status_name__iexact="Inactive").exclude(status__isnull=True).exclude(status_id__status_name__iexact="Not Renewing")
        active_customers.update(status=not_responded_status)
        return HttpResponseRedirect("renewals")

    # Purge "Inactive" Cust_Lockers
    if 'purge' in request.POST:
        inactive_lockers = Cust_Locker.objects.filter(cust_id__status_id__status_name__iexact="Inactive")
        print(inactive_lockers)
        for locker in inactive_lockers:
            print(locker)
            locker.delete()
        return HttpResponseRedirect("renewals")

    # Set Not Renewing Status to Inactive
    if 'inactive' in request.POST:
        inactive = Status.objects.get(pk=4)
        not_renewing = Customer.objects.filter(status_id__status_name__iexact="Not Renewing")
        not_renewing.update(status=inactive)
        return HttpResponseRedirect("renewals")

    if request.GET.get('featured'):
        location = request.GET['featured']
        print(location)
        all_cust_locker = all_cust_locker.filter(locker_id__location_id__location_name__contains=location).filter(cust_id__status_id__status_name__iexact="Not Responded")
    else:
        all_cust_locker = Cust_Locker.objects.filter(cust_id__status_id__status_name__iexact="Not Responded")

    # context_dict = {'listings': listings}
    # return render(request, template_name, context_dict)

    return render(request, 'renewals.html',
                  {'all_cust_lockers': all_cust_locker,
                   'all_stations': all_stations,
                   'locker_not_renewal_count_total': locker_not_renewal_count_total,
                   'locker_renewal_count_total': locker_renewal_count_total,
                   'not_responded_count_total': not_responded_count_total,
                   'total_percentage_responded': total_percentage_responded,
                   'total_lockers': total_lockers,
                   'total_occupied': total_occupied})

@staff_member_required
# TBD: DELETE IF UNIMPLEMENTED
def log(request):
    all_logs = Locker_Log.objects.all()
    return render(request, 'log.html',
                  {'all_logs': all_logs})