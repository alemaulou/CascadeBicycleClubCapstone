# Generated by Django 3.0.6 on 2020-05-11 17:02

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0028_auto_20200511_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='renewal_date',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='database.Locker_Renew_Date'),
        ),
        migrations.AlterField(
            model_name='renewal',
            name='phone_call_date',
            field=models.DateField(blank=True, default=datetime.datetime(2020, 5, 11, 17, 2, 35, 481264, tzinfo=utc), verbose_name='Phone Call Date'),
        ),
    ]
