from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
import csv, io
from django.contrib import messages
from .models import Customer, Inquiry

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def customer_upload(request):
    template = "customer_upload.html"

    prompt = {
        'order': 'order of csv should be: cust_f_name, cust_l_name, cust_email, address, city, state, zip'
    }

    if request.method == "GET":
        return render(request, template, prompt)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'This is not a csv file')

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
