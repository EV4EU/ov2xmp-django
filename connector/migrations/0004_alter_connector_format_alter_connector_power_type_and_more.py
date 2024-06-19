# Generated by Django 5.0.2 on 2024-06-19 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connector', '0003_connector_format_connector_power_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connector',
            name='format',
            field=models.CharField(blank=True, choices=[('SOCKET', 'Socket'), ('CABLE', 'Cable')], default=None, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='connector',
            name='power_type',
            field=models.CharField(blank=True, choices=[('AC_1_PHASE', 'Ac 1 Phase'), ('AC_3_PHASE', 'Ac 3 Phase'), ('DC', 'Dc')], default=None, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='connector',
            name='standard',
            field=models.CharField(blank=True, choices=[('CHADEMO', 'Chademo'), ('DOMESTIC_A', 'Domestic A'), ('IEC_60309_2_single_16', 'Iec 60309 2 Single 16'), ('IEC_62196_T1_COMBO', 'Iec 62196 T1 Combo')], default=None, max_length=255, null=True),
        ),
    ]
