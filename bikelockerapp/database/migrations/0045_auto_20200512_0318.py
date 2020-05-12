# Generated by Django 3.0.6 on 2020-05-12 03:18

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0044_auto_20200512_0002'),
    ]

    operations = [
        migrations.AddField(
            model_name='cust_locker',
            name='contacted',
            field=models.CharField(choices=[('No', 'No'), ('Initial Contact', 'Initial Contact'), ('Second Contact', 'Second Contact')], default='No', max_length=50, verbose_name='Contacted'),
        ),
        migrations.AlterField(
            model_name='renewal',
            name='phone_call_date',
            field=models.DateField(blank=True, default=datetime.datetime(2020, 5, 12, 3, 18, 36, 482246, tzinfo=utc), verbose_name='Phone Call Date'),
        ),
    ]
