# Generated by Django 3.0.6 on 2020-05-13 04:56

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0050_auto_20200512_1615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cust_locker',
            name='contacted',
            field=models.CharField(choices=[('No Contact', 'No Contact'), ('Initial Contact', 'Initial Contact'), ('Second Contact', 'Second Contact')], default='No', max_length=50, verbose_name='Contacted'),
        ),
        migrations.AlterField(
            model_name='cust_locker',
            name='renew_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='renewal',
            name='phone_call_date',
            field=models.DateField(blank=True, default=datetime.datetime(2020, 5, 13, 4, 56, 31, 932551, tzinfo=utc), verbose_name='Phone Call Date'),
        ),
    ]
