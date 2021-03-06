# Generated by Django 3.0.3 on 2020-05-07 18:22

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0028_auto_20200507_1011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cust_locker',
            name='contract_date',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='cust_locker',
            name='renew_date',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='renewal',
            name='phone_call_date',
            field=models.DateField(blank=True, default=datetime.datetime(2020, 5, 7, 18, 22, 42, 605406, tzinfo=utc), verbose_name='Phone Call Date'),
        ),
    ]
