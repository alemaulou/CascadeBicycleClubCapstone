# Generated by Django 3.0.3 on 2020-05-12 23:15

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0049_auto_20200512_1249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='renewal',
            name='phone_call_date',
            field=models.DateField(blank=True, default=datetime.datetime(2020, 5, 12, 23, 15, 48, 78065, tzinfo=utc), verbose_name='Phone Call Date'),
        ),
    ]
