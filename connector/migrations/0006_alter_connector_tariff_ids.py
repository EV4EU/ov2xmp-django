# Generated by Django 5.1.1 on 2024-12-02 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connector', '0005_connector_charging_profile_and_more'),
        ('ocpi', '0007_alter_cdr_party_id_alter_tariff_party_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connector',
            name='tariff_ids',
            field=models.ManyToManyField(default=None, to='ocpi.tariff'),
        ),
    ]
