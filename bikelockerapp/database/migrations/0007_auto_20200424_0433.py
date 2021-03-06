# Generated by Django 3.0.3 on 2020-04-24 04:33

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0006_auto_20200424_0404'),
    ]

    operations = [
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('staff_id', models.AutoField(primary_key=True, serialize=False)),
                ('staff_f_name', models.CharField(max_length=50, verbose_name='First Name')),
                ('staff_l_name', models.CharField(max_length=50, verbose_name='Last Name')),
                ('staff_email', models.EmailField(default='', max_length=100, verbose_name='Email')),
                ('staff_phone', models.CharField(default='', max_length=50, verbose_name='Phone #1')),
                ('staff_phone2', models.CharField(blank=True, default='', max_length=50, verbose_name='Phone #2')),
                ('staff_address', models.CharField(default='', max_length=50, verbose_name='Street Address')),
                ('staff_city', models.CharField(max_length=50, verbose_name='City')),
                ('staff_state', models.CharField(max_length=50, verbose_name='State')),
                ('staff_zip', models.CharField(max_length=10, verbose_name='Zip Code')),
            ],
            options={
                'ordering': ['staff_l_name'],
            },
        ),
        migrations.AlterField(
            model_name='renewal',
            name='phone_call_date',
            field=models.DateField(blank=True, default=datetime.datetime(2020, 4, 24, 4, 33, 4, 486888), verbose_name='Phone Call Date'),
        ),
        migrations.CreateModel(
            name='Locker_Log',
            fields=[
                ('locker_log_id', models.AutoField(primary_key=True, serialize=False)),
                ('action', models.CharField(max_length=500, verbose_name='Action')),
                ('action_done', models.CharField(max_length=500, verbose_name='Action Done')),
                ('next_step', models.CharField(max_length=500, verbose_name='Action')),
                ('resolved', models.BooleanField(default=False, verbose_name='Resolved')),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.Customer')),
                ('location_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.Location')),
                ('staff_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.Staff')),
            ],
        ),
    ]
