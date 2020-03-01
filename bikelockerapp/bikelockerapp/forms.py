from django import forms

from database.models import Customer

class CustomerForm(forms.ModelForm):
    lockerLocations =  (
    ('auburn', 'Auburn'),
    ('aurora-village', 'Aurora Village'),
    ('bear-creek', 'Bear Creek'),
    ('brickyard', 'Brickyard'),
    ('burien', 'Burien'),
    ('eastgate', 'Eastgate'),
    ('federal-way', 'Federal Way'),
    ('greenlake', 'Greenlake'),
    ('houghton', 'Houghton'),
    ('issaquah-pr', 'Issaquah P&R'),
    ('issaquah-highlands', 'Issaquah Highlands'),
    ('kenmore', 'Kenmore'),
    ('kent', 'Kent'),
    ('kingsgate', 'Kingsgate'),
    ('montlake', 'Montlake'),
    ('newport-hills', 'Newport Hills'),
    ('northgate', 'Northgate'),
    ('redmond-tc', 'Redmond TC'),
    ('renton-highlands', 'Renton Highlands'),
    ('so-bellevue', 'So. Bellevue'),
    ('so-kirkland', 'So. Kirkland'),
    ('so-sammamish', 'So. Sammamish'),
    ('tukwila', 'Tukwila'),
    ('vashon-island', 'Vashon Island'),
    ('woodinville', 'Woodinville')
    )

    locations = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          choices=lockerLocations)
    class Meta:
        model = Customer
        fields = ['cust_f_name', 'cust_l_name', 'cust_email', 'cust_address', 'cust_city', 'cust_state', 'cust_zip', 'locations']