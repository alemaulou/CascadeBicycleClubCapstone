# Generated by Django 3.0.6 on 2020-05-07 09:21

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0020_auto_20200507_0350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cust_locker',
            name='description',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='location',
            name='location_zip',
            field=models.CharField(blank=True, max_length=10, verbose_name='Location Zip'),
        ),
        migrations.AlterField(
            model_name='renewal',
            name='phone_call_date',
            field=models.DateField(blank=True, default=datetime.datetime(2020, 5, 7, 9, 21, 28, 230369, tzinfo=utc), verbose_name='Phone Call Date'),
        ),
        migrations.CreateModel(
            name='Renewal_Form',
            fields=[
                ('renewal_form_id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(default='', max_length=254)),
                ('mailing_address', models.CharField(default='', max_length=300, verbose_name='Current Mailing Address')),
                ('phone', models.CharField(default='', max_length=50, verbose_name='Phone')),
                ('locker_number', models.CharField(default='', max_length=50, verbose_name='Locker Number')),
                ('locker_usage', models.CharField(choices=[('0-1', '0-1'), ('1-2', '1-2'), ('2-3', '2-3'), ('3+', '3+')], max_length=50, verbose_name='Locker Usage')),
                ('renewal_decision', models.CharField(choices=[(True, 'Yes'), (False, 'No')], max_length=50, verbose_name='Renewal Decision')),
                ('feedback', models.TextField(default='', max_length=5000, verbose_name='Feedback')),
                ('locations', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.Location')),
            ],
        ),
    ]