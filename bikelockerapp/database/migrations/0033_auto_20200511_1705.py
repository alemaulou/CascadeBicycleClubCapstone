# Generated by Django 3.0.6 on 2020-05-11 17:05

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0032_auto_20200511_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='renewal',
            name='phone_call_date',
            field=models.DateField(blank=True, default=datetime.datetime(2020, 5, 11, 17, 5, 17, 549697, tzinfo=utc), verbose_name='Phone Call Date'),
        ),
    ]
