# Generated by Django 5.0.2 on 2024-05-08 02:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chargepoint', '0004_chargepoint_chargepoint_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chargepoint',
            name='chargepoint_type',
        ),
    ]