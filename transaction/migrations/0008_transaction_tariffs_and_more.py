# Generated by Django 5.1.1 on 2024-12-02 20:08

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0007_transaction_chargingprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='tariffs',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.JSONField(), blank=True, default=None, null=True, size=None),
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='chargingprofile',
        ),
        migrations.AddField(
            model_name='transaction',
            name='chargingprofile',
            field=models.JSONField(blank=True, default=None, null=True),
        ),
    ]
