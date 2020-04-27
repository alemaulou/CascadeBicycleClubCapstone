# Generated by Django 3.0.3 on 2020-04-24 04:58

import datetime
from django.db import migrations, models
import django.utils.timezone
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0008_auto_20200424_0434'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='locker_log',
            options={'verbose_name': 'Locker Log', 'verbose_name_plural': 'Locker Logs'},
        ),
        migrations.AddField(
            model_name='locker_log',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='locker_log',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='locker_log',
            name='action',
            field=models.CharField(blank=True, max_length=500, verbose_name='Action'),
        ),
        migrations.AlterField(
            model_name='locker_log',
            name='action_done',
            field=models.CharField(blank=True, max_length=500, verbose_name='Action Done'),
        ),
        migrations.AlterField(
            model_name='locker_log',
            name='next_step',
            field=models.CharField(blank=True, max_length=500, verbose_name='Action'),
        ),
        migrations.AlterField(
            model_name='renewal',
            name='phone_call_date',
            field=models.DateField(blank=True, default=datetime.datetime(2020, 4, 24, 4, 57, 59, 541885, tzinfo=utc), verbose_name='Phone Call Date'),
        ),
    ]
