# Generated by Django 4.2.4 on 2024-01-10 22:07

from django.db import migrations, models
import timezone_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0002_alter_location_country_alter_location_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='residential',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='location',
            name='timezone',
            field=timezone_field.fields.TimeZoneField(default='Europe/Athens'),
        ),
    ]
