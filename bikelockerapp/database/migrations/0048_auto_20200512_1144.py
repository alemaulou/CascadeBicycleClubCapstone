# Generated by Django 3.0.3 on 2020-05-12 18:44

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0047_auto_20200512_1141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='renewal',
            name='phone_call_date',
            field=models.DateField(blank=True, default=datetime.datetime(2020, 5, 12, 18, 44, 36, 984328, tzinfo=utc), verbose_name='Phone Call Date'),
        ),
    ]