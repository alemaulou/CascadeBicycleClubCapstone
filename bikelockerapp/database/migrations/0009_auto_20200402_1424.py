# Generated by Django 3.0.3 on 2020-04-02 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0008_auto_20200402_1325'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='maintenance',
            name='isWholeLocation',
        ),
        migrations.AddField(
            model_name='maintenance',
            name='maintenance_scope',
            field=models.CharField(choices=[('general facility', 'General Facility'), ('specific locker(s)', 'Specific Locker(s)')], default='general facility', max_length=50, verbose_name='Maintenance Scope'),
            preserve_default=False,
        ),
    ]
