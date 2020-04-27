# Generated by Django 3.0.3 on 2020-04-25 09:10

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0011_auto_20200425_0857'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='database.Status'),
        ),
        migrations.AddField(
            model_name='status',
            name='status_desc',
            field=models.CharField(blank=True, max_length=100, verbose_name='Status Description'),
        ),
        migrations.AlterField(
            model_name='renewal',
            name='phone_call_date',
            field=models.DateField(blank=True, default=datetime.datetime(2020, 4, 25, 9, 10, 29, 966083, tzinfo=utc), verbose_name='Phone Call Date'),
        ),
        migrations.AlterField(
            model_name='status',
            name='status_name',
            field=models.CharField(max_length=100, verbose_name='Status Name'),
        ),
    ]
