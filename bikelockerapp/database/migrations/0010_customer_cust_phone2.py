# Generated by Django 3.0.3 on 2020-04-09 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0009_auto_20200408_0029'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='cust_phone2',
            field=models.CharField(default='', max_length=50, verbose_name='Phone'),
        ),
    ]
