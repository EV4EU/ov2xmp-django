# Generated by Django 5.1.1 on 2025-01-21 11:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('connector', '0007_connector_charging_profile_array'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='connector',
            name='charging_profile',
        ),
        migrations.RemoveField(
            model_name='connector',
            name='charging_profile_array',
        ),
    ]
