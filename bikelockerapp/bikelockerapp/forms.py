from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from database.models import Customer, Location

class CustomerForm(forms.ModelForm):

    locations = forms.ModelMultipleChoiceField(queryset=Location.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Customer
        fields = ['cust_f_name', 'cust_l_name', 'cust_email', 'cust_address', 'cust_city', 'cust_state', 'cust_zip', 'locations']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('cust_f_name', css_class='form-group col-md-6 mb-0'),
                Column('cust_l_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'cust_address',
            Row(
                Column('cust_city', css_class='form-group col-md-6 mb-0'),
                Column('cust_state', css_class='form-group col-md-4 mb-0'),
                Column('cust_zip', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            'cust_email',
            'locations',
            Submit('submit', 'Submit')
        )
