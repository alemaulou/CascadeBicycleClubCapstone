import csv, io
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail
from django.shortcuts import render
from django.http import HttpResponseRedirect, BadHeaderError, HttpResponse
from django.contrib import messages
from .models import Customer, Inquiry, Location, Cust_Locker, Maintenance, Locker, Waitlist, Locker_Log, Status, \
    Locker_Status, Renewal_Form
from .forms import CustomerForm, SendEmailForm, SendEmailFormAfter2Weeks, RenewalsForm
from datetime import datetime, date, timedelta
from django.conf import settings

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

    render_cust = False
    if location_contains_query or customer_contains_query:
        render_cust = True

    # Filtering customer data (station, locker, inquiry) by location
    if location_contains_query != '' and location_contains_query is not None:
        all_cust_locker = all_cust_locker.filter(locker_id__location_id__location_name__contains=location_contains_query)
        all_inquiry = all_inquiry.filter(locations__location_name__contains=location_contains_query)
        all_maintenance = all_maintenance.filter(lockers__location_id__location_name__contains=location_contains_query)

    # Filtering customer data by customer name
    if customer_contains_query != '' and customer_contains_query is not None:
        customers = []
        if all_cust_locker.filter(cust_id__cust_f_name__icontains=customer_contains_query) | all_cust_locker.filter(cust_id__cust_l_name__icontains=customer_contains_query) | all_cust_locker.filter(cust_id__cust_email__icontains=customer_contains_query):
            customers += all_cust_locker.filter(cust_id__cust_f_name__icontains=customer_contains_query)
            customers += all_cust_locker.filter(cust_id__cust_l_name__icontains=customer_contains_query)
            customers += all_cust_locker.filter(cust_id__cust_email__icontains=customer_contains_query)
        all_cust_locker = customers
        all_inquiry = all_inquiry.filter(cust_id__cust_f_name__contains=customer_contains_query)

    # Rendering boolean for Locker Renewals
    contains_locker_renewals = False
    for locker_renewals in all_cust_locker:
        if locker_renewals.location_renewal:
            if date.today() > locker_renewals.location_renewal.date:
                contains_locker_renewals = True
        else:
            pass

    # Returning values to to render onto template
    render_dicts = {'render_cust': render_cust, 'all_stations': all_station, 'all_customer': all_customer, 'all_inquiries': all_inquiry, 'all_cust_lockers': all_cust_locker, 'locker_renewals': contains_locker_renewals, 'all_maintenance' : all_maintenance}
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
        not_created, created = Customer.objects.update_or_create(
            cust_f_name = column[0],
            cust_l_name = column[1],
            cust_email = column[6],
            cust_phone = column[8].replace('-',''),
            cust_phone2 = column[9].replace('-',''),
            cust_address = column[2],
            cust_city = column[3],
            cust_state = column[4],
            cust_zip = column[5]
        )

        not_created_location, created_location = Location.objects.update_or_create(
            location_name = column[15],
            location_capacity = 0
        )
        not_created_locker, created_locker = Locker.objects.update_or_create(
            location_id = not_created_location,
            locker_name = column[10],
            locker_status_id =  Locker_Status.objects.get(locker_status_name='Leased')
        )
        contract_date = column[13]
        contract_date_year = contract_date[-2:]
        contract_date = contract_date[:-2]
        contract_date += "20{}".format(contract_date_year)

        if not_created.cust_f_name != "":
            not_created_cust_locker, created_cust_locker = Cust_Locker.objects.update_or_create(
                cust_id = not_created,
                locker_id = not_created_locker,
                locker_id__locker_status_id = Locker_Status.objects.get(locker_status_name='Leased'),
                contract_date = datetime.strptime(contract_date, "%m/%d/%Y").date(),
                renew_date = datetime.now(),
                description = column[11]
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
    x = [obj.cust_id.cust_email for obj in Cust_Locker.objects.all() if (obj.is_under_2_weeks_past_due and obj.not_contacted)]
    yy = [obj for obj in Cust_Locker.objects.all() if obj.is_2_weeks_past_due and (obj.not_contacted)]
    y = [obj.cust_id.cust_email for obj in yy if obj.contacted_once]
    for yy in y:
        print(yy)
    all_stations = Location.objects.all()
    all_cust_locker = Cust_Locker.objects.all()
    if request.method == 'GET':
        form = SendEmailForm()
        form2 = SendEmailFormAfter2Weeks()
    if request.method == 'POST' and 'form1' in request.POST:
        form = SendEmailForm(request.POST or None)
        if form.is_valid():
            print('test')
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            from_email = settings.EMAIL_HOST_USER
            try:
                send_mail(subject, message, from_email, x, fail_silently=False)
                customers = [obj for obj in Cust_Locker.objects.all() if
                     (obj.is_under_2_weeks_past_due and obj.not_contacted)]
                for customer in customers:
                    print(customer)
                    print(customer.contacted)
                    customer.contacted = 'Initial Contact'
                    customer.save()
                    print(customer.contacted)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return HttpResponseRedirect("send_email")

    if request.method == 'POST' and 'form2' in request.POST:
        print('test')
        form2 = SendEmailFormAfter2Weeks(request.POST)
        if form2.is_valid():
            print('test2')
            subject = form2.cleaned_data['subject']
            message = form2.cleaned_data['message']
            from_email = settings.EMAIL_HOST_USER
            try:
                send_mail(subject, message, from_email, y, fail_silently=False)
                customers = [obj for obj in Cust_Locker.objects.all() if
                             (obj.is_2_weeks_past_due and obj.not_contacted)]
                customers_filtered = [obj for obj in customers if obj.contacted_once]
                for customer in customers_filtered:
                    print(customer)
                    print(customer.contacted)
                    customer.contacted = 'Second Contact'
                    customer.save()
                    print(customer.contacted)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return HttpResponseRedirect("send_email")

    if 'reset contacted' in request.POST:
        print('tester')
        active_customers = Customer.objects.all().exclude(status_id__status_name__iexact="Inactive").exclude(status__isnull=True).exclude(status_id__status_name__iexact="Not Renewing")
        active_lockers = Cust_Locker.objects.all().filter(cust_id__in=active_customers)
        for customer in active_lockers:
            if customer.location_renewal:
                if date.today() > customer.location_renewal.date:
                    customer.contacted = "No"
                    customer.save()
                else:
                    pass
            else:
                pass
        return HttpResponseRedirect("send_email")

    # Rendering boolean for Locker Renewals
    contains_locker_renewals = False
    for locker_renewals in all_cust_locker:
        if locker_renewals.location_renewal:
            if date.today() > locker_renewals.location_renewal.date:
                contains_locker_renewals = True
        else:
            pass

    # Rendering boolean for New Locker Renewal Requests
    contains_lr_under_2_weeks = False
    for locker_renewals in all_cust_locker:
        if locker_renewals.location_renewal:
            if date.today() > locker_renewals.location_renewal.date and date.today() - timedelta(14) < locker_renewals.location_renewal.date and locker_renewals.contacted == "No":
                contains_lr_under_2_weeks = True
        else:
            pass

    # Rendering boolean for Past due (over 2 week) Locker Renewal Requests
    contains_lr_over_2_weeks = False
    for locker_renewals in all_cust_locker:
        if locker_renewals.location_renewal:
            if date.today() - timedelta(14) > locker_renewals.location_renewal.date and (locker_renewals.contacted == "No" or locker_renewals.contacted == "Initial Contact"):
                contains_lr_over_2_weeks = True
        else:
            pass

    # Total number of Lockers by Location Capacity
    total_lockers = 0
    for location in all_stations:
        total_lockers += location.location_capacity

    # Total number of Occupied Lockers
    total_occupied = len(Cust_Locker.objects.all())

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

    # Total number of Lockers by Location Capacity
    total_lockers = 0
    for location in all_stations:
        total_lockers += location.location_capacity

    # Total number of Occupied Lockers
    total_occupied = len(Cust_Locker.objects.all())

    ## Get Total Customer Renewal Status to render
    # Total Renewing
    locker_renewal_count_total = 0

    for locker in all_stations:
        if locker.pk:
            try:
                bug = Cust_Locker.objects.filter(locker_id__location_id=locker.pk)
                type(bug)
                status = Status.objects.get(status_name='Renewed')
                locker_renewal_count_total += len(Cust_Locker.objects.filter(locker_id__location_id=locker.pk).filter(cust_id__status_id__status_name=str(status)))
            except Cust_Locker.DoesNotExist:
                pass

    # Not Renewing
    locker_not_renewal_count_total = 0
    for locker in all_stations:
        if locker.pk:
            try:
                status = Status.objects.get(status_name='Not Renewing')
                locker_not_renewal_count_total += len(Cust_Locker.objects.filter(locker_id__location_id=locker.pk).filter(cust_id__status_id__status_name=str(status)))
            except Cust_Locker.DoesNotExist:
                pass

    # Not Responded
    not_responded_count_total = 0
    for locker in all_stations:
        if locker.pk:
            try:
                status = Status.objects.get(status_name='Not Responded')
                not_responded_count_total += len(Cust_Locker.objects.filter(locker_id__location_id=locker.pk).filter(cust_id__status_id__status_name=str(status)))
            except Cust_Locker.DoesNotExist:
                pass

    # Calculation for number responded and total
    total_percentage_responded = 0
    if (locker_renewal_count_total + locker_not_renewal_count_total + not_responded_count_total) != 0:
        total_percentage_responded = str(round((locker_renewal_count_total + locker_not_renewal_count_total) / (locker_renewal_count_total + locker_not_renewal_count_total + not_responded_count_total),2)*100) + "%"
    else:
        total_percentage_responded = str(0) + "%"

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

    # Update Renewal date based on location.
    list_of_location = Location.objects.all()
    list_of_cust_locker = Cust_Locker.objects.filter(locker_id__location_id__in=list_of_location)
    if 'update_renewal' in request.POST:
        return HttpResponseRedirect("location_renewals")
    # Mass update
    if 'list' in request.POST:
        active_customers = Customer.objects.all().exclude(status_id__status_name__iexact="Inactive").exclude(status__isnull=True).exclude(status_id__status_name__iexact="Not Renewing")
        type(active_customers)
        active_lockers = Cust_Locker.objects.all().filter(cust_id__in=active_customers)
        for customer in active_lockers:
            if customer.location_renewal:
                if date.today() > customer.location_renewal.date:
                    print(customer.cust_id.status)
                    customer.cust_id.status=not_responded_status
                    customer.cust_id.save()
                else:
                    pass
            else:
                pass
        return HttpResponseRedirect("renewals")

    # Purge "Inactive" Cust_Lockers
    if 'purge' in request.POST:
        inactive_lockers = Cust_Locker.objects.filter(cust_id__status_id__status_name__iexact="Inactive")
        for single_locker in inactive_lockers:
            locker_available = Locker_Status.objects.get(locker_status_name='Available')
            inactive = Locker.objects.filter(locker_id = single_locker.pk)
            inactive.update(locker_status_id=locker_available)
            single_locker.delete()
        return HttpResponseRedirect("renewals")

    # Set Not Renewing Status to Inactive
    if 'inactive' in request.POST:
        inactive = Status.objects.get(pk=4)
        not_renewing = Customer.objects.filter(status_id__status_name__iexact="Not Renewing")
        not_renewing.update(status=inactive)
        return HttpResponseRedirect("renewals")

    if request.GET.get('featured'):
        location = request.GET['featured']
        all_cust_locker = all_cust_locker.filter(locker_id__location_id__location_name__contains=location).filter(cust_id__status_id__status_name__iexact="Not Responded")
    else:
        all_cust_locker = Cust_Locker.objects.filter(cust_id__status_id__status_name__iexact="Not Responded")

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

def renewals_form(request):
    submitted = False
    if request.method == 'POST':
        print('did')
        form = RenewalsForm(request.POST)
        if form.is_valid():
            product = form.save()
            return HttpResponseRedirect('/admin')
        else:
            print(form.errors)
    else:
        form = RenewalsForm()
        if request.method == 'GET':
            submitted = True
    return render(request, 'renewals_form.html', {'form': form})