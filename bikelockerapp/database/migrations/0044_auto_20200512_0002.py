# Generated by Django 3.0.6 on 2020-05-12 00:02

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0043_auto_20200511_2355'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='location_renewal_day',
        ),
        migrations.RemoveField(
            model_name='location_renewals',
            name='location_renew_name',
        ),
        migrations.AddField(
            model_name='location_renewals',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='database.Location'),
        ),
        migrations.AlterField(
            model_name='renewal',
            name='phone_call_date',
            field=models.DateField(blank=True, default=datetime.datetime(2020, 5, 12, 0, 2, 44, 889163, tzinfo=utc), verbose_name='Phone Call Date'),
        ),
    ]
