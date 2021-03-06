# Generated by Django 3.0.6 on 2020-05-07 10:19

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0023_auto_20200507_1008'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='renewal_form',
            name='locations',
        ),
        migrations.AddField(
            model_name='renewal_form',
            name='location',
            field=models.CharField(default='', max_length=50, verbose_name='Location'),
        ),
        migrations.AlterField(
            model_name='renewal',
            name='phone_call_date',
            field=models.DateField(blank=True, default=datetime.datetime(2020, 5, 7, 10, 19, 20, 621099, tzinfo=utc), verbose_name='Phone Call Date'),
        ),
    ]
