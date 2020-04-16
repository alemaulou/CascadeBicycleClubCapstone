from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
import csv, io
from django.contrib import messages
from .models import Customer, Inquiry, Location, Cust_Locker, Maintenance
from .forms import CustomerForm
from datetime import datetime

def index(request):
    template_name = 'admin/index.html'
    all_inquiry = Inquiry.objects.all()
    all_station = Location.objects.all()
    all_customer = Customer.objects.all()
    all_cust_locker = Cust_Locker.objects.all()
    all_maintenance = Maintenance.objects.all()
    location_contains_query = request.GET.get('location')
    customer_contains_query = request.GET.get('customer')


    if location_contains_query != '' and location_contains_query is not None:
        all_station = all_station.filter(location_name__icontains=location_contains_query)
        all_cust_locker = all_cust_locker.filter(locker_id__location_id__location_name__contains=location_contains_query)
        all_inquiry = all_inquiry.filter(locations__location_name__contains=location_contains_query)
        all_maintenance = all_maintenance.filter(locations__location_name__contains=location_contains_query)
 
    if customer_contains_query != '' and customer_contains_query is not None:
        all_customer = all_customer.filter(cust_f_name__icontains=customer_contains_query)

    sta = {'all_stations': all_station, 'all_customer': all_customer, 'all_inquiries': all_inquiry, 'all_cust_lockers': all_cust_locker, 'all_maintenance': all_maintenance}
    return render(request, 'admin/index.html', sta)

def BootstrapFilterView(request):
    render(request, "bootstrap_form.html ")

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


