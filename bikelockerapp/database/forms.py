from django import forms

from database.models import Customer, Location

class SendEmailForm(forms.Form):
    subject = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': ('Subject')}))
    message = forms.CharField(widget=forms.Textarea)
    users = forms.ModelMultipleChoiceField(label="To",
                                           queryset=Customer.objects.all(),
                                           widget=forms.SelectMultiple())


class CustomerForm(forms.ModelForm):
    locations = forms.ModelMultipleChoiceField(queryset=Location.objects.all(), widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Customer
        fields = ['cust_f_name', 'cust_l_name', 'cust_email', 'cust_address', 'cust_city', 'cust_state', 'cust_zip', 'locations']