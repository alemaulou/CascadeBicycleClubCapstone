# Generated by Django 3.0.3 on 2020-04-24 03:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0004_auto_20200423_2056'),
    ]

    operations = [
        migrations.AddField(
            model_name='locker',
            name='locker_capacity',
            field=models.IntegerField(default=0, verbose_name='Locker Capacity'),
        ),
        migrations.AlterField(
            model_name='renewal',
            name='phone_call_date',
            field=models.DateField(blank=True, default=datetime.datetime(2020, 4, 24, 3, 31, 16, 917784), verbose_name='Phone Call Date'),
        ),
    ]