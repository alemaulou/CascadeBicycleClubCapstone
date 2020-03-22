from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from database.models import Customer, Inquiry
from .forms import CustomerForm
from datetime import datetime

def customer_inquiry(request):
    submitted = False
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            identity = customer.pk
            locs = form.cleaned_data['locations']
            obj = Customer.objects.get(cust_id=identity)
            inquiry = Inquiry.objects.create(
                cust_id = Customer.objects.get(cust_id = obj.pk),
                inquiry_date = datetime.now())
            inquiry.locations.add(*locs)
            return HttpResponseRedirect('/customer_inquiry/?submitted=True')
    else:
        form = CustomerForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'customer_inquiry.html', {'form': form, 'submitted': submitted})