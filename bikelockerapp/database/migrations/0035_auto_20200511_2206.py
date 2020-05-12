# Generated by Django 3.0.6 on 2020-05-11 22:06

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0034_auto_20200511_1707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='database.Status'),
        ),
        migrations.AlterField(
            model_name='renewal',
            name='phone_call_date',
            field=models.DateField(blank=True, default=datetime.datetime(2020, 5, 11, 22, 6, 0, 572515, tzinfo=utc), verbose_name='Phone Call Date'),
        ),
    ]