from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from database.models import Customer, Location, Maintenance
from django_select2 import forms as s2forms

class CustomerForm(forms.ModelForm):
    locations = forms.ModelMultipleChoiceField(queryset=Location.objects.all(), widget=s2forms.Select2MultipleWidget)
    class Meta:
        model = Customer
        fields = ['cust_f_name', 'cust_l_name', 'cust_email', 'cust_phone', 'cust_phone2', 'cust_address', 'cust_city', 'cust_state', 'cust_zip', 'locations']
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

class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        fields = ['location_id', 'main_type_id', 'maintenance_scope', 'lockers', 'maintenance_description', 'start_date']
    def __init__(self, *args, **kwargs):
        super(MaintenanceForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.maintenance_scope == 'general facility' :
            self.fields['lockers'].disabled = True # still displays the field in the template
        