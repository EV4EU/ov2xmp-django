# Generated by Django 5.0.2 on 2024-05-08 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0005_rename_street_address_location_address_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='location',
            old_name='uuid',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='location',
            old_name='timezone',
            new_name='time_zone',
        ),
        migrations.AddField(
            model_name='location',
            name='country_code',
            field=models.CharField(default='GR', max_length=2),
        ),
        migrations.AddField(
            model_name='location',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='location',
            name='parking_type',
            field=models.CharField(choices=[('ALONG_MOTORWAY', 'Along Motorway'), ('PARKING_GARAGE', 'Parking Garage'), ('PARKING_LOT', 'Parking Lot'), ('ON_DRIVEWAY', 'On Driveway'), ('ON_STREET', 'On Street'), ('UNDERGROUND_GARAGE', 'Underground Garage')], default='PARKING_LOT', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='location',
            name='party_id',
            field=models.CharField(default='DEF', max_length=3),
        ),
        migrations.AddField(
            model_name='location',
            name='state',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
