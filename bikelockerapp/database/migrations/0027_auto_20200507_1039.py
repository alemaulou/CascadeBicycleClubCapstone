# Generated by Django 3.0.6 on 2020-05-07 10:39

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0026_auto_20200507_1037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='renewal',
            name='phone_call_date',
            field=models.DateField(blank=True, default=datetime.datetime(2020, 5, 7, 10, 39, 7, 106751, tzinfo=utc), verbose_name='Phone Call Date'),
        ),
    ]