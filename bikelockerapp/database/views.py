import csv, io
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, BadHeaderError, HttpResponse
from django.contrib import messages
from .models import Customer, Inquiry, Location, Cust_Locker, Waitlist, Locker
from .forms import CustomerForm, SendEmailForm, SendEmailFormAfter2Weeks
from datetime import datetime, date, timedelta
from django.conf import settings

# Admin Index View
def index(request):

    # Querying for data
    all_inquiry = Inquiry.objects.all()
    all_station = Location.objects.all()
    all_customer = Customer.objects.all()
    all_cust_locker = Cust_Locker.objects.all()

    # Checking to see if user input in search field "contains" query
    location_contains_query = request.GET.get('location')
    customer_contains_query = request.GET.get('customer')

    # Filtering customer data (station, locker, inquiry) by location
    if location_contains_query != '' and location_contains_query is not None:
        all_station = all_station.filter(location_name__icontains=location_contains_query)
        all_cust_locker = all_cust_locker.filter(locker_id__location_id__location_name__contains=location_contains_query)
        all_inquiry = all_inquiry.filter(locations__location_name__contains=location_contains_query)

    # Filtering customer data by customer name
    if customer_contains_query != '' and customer_contains_query is not None:
        all_customer = all_customer.filter(cust_f_name__icontains=customer_contains_query)


    # Rendering boolean for Locker Renewals
    contains_locker_renewals = False
    for locker_renewals in all_cust_locker:
        if date.today() > locker_renewals.renew_date:
            contains_locker_renewals = True

    # Returning values to to render onto template
    render_dicts = {'all_stations': all_station, 'all_customer': all_customer, 'all_inquiries': all_inquiry, 'all_cust_lockers': all_cust_locker, 'locker_renewals': contains_locker_renewals}
    return render(request, 'admin/index.html', render_dicts)

def BootstrapFilterView(request):
    render(request, "bootstrap_form.html ")

# Customer Upload Data View
def customer_upload(request):
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
def send_email(request):
    x = [obj.cust_id.cust_email for obj in Cust_Locker.objects.all() if obj.is_under_2_weeks_past_due]
    y = [obj.cust_id.cust_email for obj in Cust_Locker.objects.all() if obj.is_2_weeks_past_due]
    all_stations = Location.objects.all()
    total_locker_count = Cust_Locker.objects.count()
    all_cust_locker = Cust_Locker.objects.all()
    if request.method == 'GET':
        form = SendEmailForm()
        form2 = SendEmailFormAfter2Weeks()
    if request.method == 'POST' and 'form1' in request.POST:
        print("test")
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
        print("test")
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


    contains_lr_under_2_weeks = False
    for locker_renewals in all_cust_locker:
        if date.today() > locker_renewals.renew_date and date.today() - timedelta(14) < locker_renewals.renew_date:
            contains_lr_under_2_weeks = True

    contains_lr_over_2_weeks = False
    for locker_renewals in all_cust_locker:
        if date.today() - timedelta(14) > locker_renewals.renew_date:
            contains_lr_over_2_weeks = True

    return render(request, 'send_email.html', {'all_stations': all_stations, 'form': form, 'form2': form2, 'emails': x, '2_weeks': y, 'all_cust_lockers': all_cust_locker, 'locker_renewals': contains_locker_renewals, 'lr_over_2': contains_lr_over_2_weeks, 'lr_under_2': contains_lr_under_2_weeks, "total_locker_count": total_locker_count})