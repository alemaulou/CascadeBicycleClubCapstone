# Generated by Django 3.0.3 on 2020-05-07 03:50

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0019_auto_20200507_0326'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='contacted',
        ),
        migrations.AlterField(
            model_name='renewal',
            name='phone_call_date',
            field=models.DateField(blank=True, default=datetime.datetime(2020, 5, 7, 3, 50, 57, 360530, tzinfo=utc), verbose_name='Phone Call Date'),
        ),
    ]