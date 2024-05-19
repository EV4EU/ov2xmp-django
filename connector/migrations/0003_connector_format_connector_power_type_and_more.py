# Generated by Django 5.0.2 on 2024-05-08 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connector', '0002_alter_connector_uuid'),
        ('ocpi', '0002_alter_tariff_id_alter_tariff_last_updated_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='connector',
            name='format',
            field=models.CharField(choices=[('SOCKET', 'Socket'), ('CABLE', 'Cable')], default='SOCKET', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='connector',
            name='power_type',
            field=models.CharField(choices=[('AC_1_PHASE', 'Ac 1 Phase'), ('AC_3_PHASE', 'Ac 3 Phase'), ('DC', 'Dc')], default='AC_3_PHASE', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='connector',
            name='standard',
            field=models.CharField(choices=[('CHADEMO', 'Chademo'), ('DOMESTIC_A', 'Domestic A'), ('IEC_60309_2_single_16', 'Iec 60309 2 Single 16'), ('IEC_62196_T1_COMBO', 'Iec 62196 T1 Combo')], default='CHADEMO', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='connector',
            name='tariff_ids',
            field=models.ManyToManyField(to='ocpi.tariff'),
        ),
    ]
