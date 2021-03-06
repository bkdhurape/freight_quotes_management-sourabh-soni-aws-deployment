# Generated by Django 2.2.5 on 2020-04-23 09:52

import datetime
from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import quote.managers.quote_manager


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0006_auto_20200221_1212'),
        ('commodity', '0001_initial'),
        ('quote', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='expected_delivery_date',
            field=models.DateField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(datetime.date(2020, 4, 23))]),
        ),
        migrations.AlterField(
            model_name='quote',
            name='quote_deadline',
            field=models.DateField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(datetime.date(2020, 4, 23))]),
        ),
        migrations.CreateModel(
            name='PackageDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(default='system', max_length=512)),
                ('updated_by', models.CharField(default='system', max_length=512)),
                ('status', models.IntegerField(choices=[(0, 'Inactive'), (1, 'Active')], default=1)),
                ('product', models.CharField(blank=True, max_length=255, null=True)),
                ('type', models.CharField(blank=True, choices=[('bale', 'BALE'), ('bundles', 'BUNDLES'), ('carton', 'CARTON'), ('pallte', 'PALLET'), ('case', 'CASE'), ('drums', 'DRUMS'), ('sack', 'SACK'), ('bag', 'BAG'), ('unpacked', 'UNPACKED')], max_length=255, null=True)),
                ('quantity', models.PositiveIntegerField(blank=True, null=True)),
                ('length', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('width', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('height', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('dimension_unit', models.CharField(choices=[('feet', 'FEET'), ('inch', 'INCH'), ('cm', 'CM'), ('mm', 'MM'), ('m', 'M')], default=None, max_length=255, null=True)),
                ('weight', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('weight_unit', models.CharField(choices=[('tons', 'TONS'), ('lbs', 'LBS')], default=None, max_length=255, null=True)),
                ('is_hazardous', models.BooleanField(default=False)),
                ('is_stackable', models.BooleanField(default=False)),
                ('container_type', models.CharField(blank=True, choices=[('20_gp', '20 GP'), ('20_flat_rack', '20 FLAT-RACK'), ('20_ot', '20 OT'), ('20_reefer', '20 REEFER'), ('20_tank', '20 TANK'), ('40_gp', '40 GP'), ('40_flat_rack', '40 FLAT-RACK'), ('40_ot', '40 OT'), ('40_reefer', '40 REEFER'), ('40_hc', '40 HC'), ('45_hc', '45 HC')], max_length=255, null=True)),
                ('no_of_containers', models.PositiveIntegerField(blank=True, null=True)),
                ('stuffing', models.CharField(blank=True, choices=[('dock', 'DOCK'), ('factory', 'FACTORY')], max_length=255, null=True)),
                ('destuffing', models.CharField(blank=True, choices=[('dock', 'DOCK'), ('factory', 'FACTORY')], max_length=255, null=True)),
                ('commodity', models.ManyToManyField(db_table='package_details_commodities', to='commodity.Commodity')),
                ('drop_location_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='address.Address')),
                ('pickup_location_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='address.Address')),
                ('quote', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='quote.Quote')),
                ('transport_mode', models.ManyToManyField(related_name='transport_mode_package_details', to='quote.QuoteTransportMode')),
            ],
            options={
                'db_table': 'package_details',
            },
            bases=(models.Model, quote.managers.quote_manager.PackageDetailsManager),
        ),
    ]
