# Generated by Django 3.0.3 on 2020-04-24 04:34

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0007_auto_20200424_0433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='renewal',
            name='phone_call_date',
            field=models.DateField(blank=True, default=datetime.datetime(2020, 4, 24, 4, 34, 25, 70380, tzinfo=utc), verbose_name='Phone Call Date'),
        ),
    ]