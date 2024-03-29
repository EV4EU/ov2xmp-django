# Generated by Django 4.2 on 2023-06-28 08:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('chargepoint', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Connector',
            fields=[
                ('uuid', models.UUIDField(primary_key=True, serialize=False)),
                ('connectorid', models.IntegerField()),
                ('availability_status', models.CharField(choices=[('Inoperative', 'Inoperative'), ('Operative', 'Operative')], default='Operative', max_length=11)),
                ('connector_status', models.CharField(choices=[('Available', 'Available'), ('Preparing', 'Preparing'), ('Charging', 'Charging'), ('SuspendedEVSE', 'SuspendedEVSE'), ('SuspendedEV', 'SuspendedEV'), ('Finishing', 'Finishing'), ('Reserved', 'Reserved'), ('Unavailable', 'Unavailable'), ('Faulted', 'Faulted')], default='Available', max_length=13)),
                ('chargepoint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chargepoint.chargepoint')),
            ],
        ),
    ]
