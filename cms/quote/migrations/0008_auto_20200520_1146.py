# Generated by Django 2.2.5 on 2020-05-20 11:46

import datetime
from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import quote.managers.quote_manager
import utils.base_models
import utils.helpers


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0006_auto_20200221_1212'),
        ('quote', '0007_auto_20200518_1030'),
    ]

    operations = [
        migrations.AddField(
            model_name='packagedetails',
            name='package_detail_type',
            field=models.CharField(choices=[('package', 'Package'), ('total', 'Total')], default='package', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='packagedetails',
            name='total_volume',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))]),
        ),
        migrations.AddField(
            model_name='packagedetails',
            name='total_volume_unit',
            field=models.CharField(choices=[('cbm', 'CBM')], default=None, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='packagedetails',
            name='total_volumetric_weight',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))]),
        ),
        migrations.AddField(
            model_name='packagedetails',
            name='total_volumetric_weight_unit',
            field=models.CharField(choices=[('kg', 'KGS')], default=None, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='packagedetails',
            name='total_weight',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))]),
        ),
        migrations.AddField(
            model_name='packagedetails',
            name='total_weight_unit',
            field=models.CharField(choices=[('kg', 'KG'), ('tonnes', 'TONS'), ('lbs', 'LBS')], default=None, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='quotetransportmode',
            name='total_volume',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))]),
        ),
        migrations.AddField(
            model_name='quotetransportmode',
            name='total_volume_unit',
            field=models.CharField(choices=[('cbm', 'CBM')], default=None, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='quotetransportmode',
            name='total_volumetric_weight',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))]),
        ),
        migrations.AddField(
            model_name='quotetransportmode',
            name='total_volumetric_weight_unit',
            field=models.CharField(choices=[('kg', 'KGS')], default=None, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='quotetransportmode',
            name='total_weight',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))]),
        ),
        migrations.AddField(
            model_name='quotetransportmode',
            name='total_weight_unit',
            field=models.CharField(choices=[('kg', 'KG'), ('tonnes', 'TONS'), ('lbs', 'LBS')], default=None, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='packagedetails',
            name='weight_unit',
            field=models.CharField(choices=[('kg', 'KG'), ('tonnes', 'TONS'), ('lbs', 'LBS')], default=None, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='quote',
            name='expected_delivery_date',
            field=models.DateField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(datetime.date(2020, 5, 20))]),
        ),
        migrations.AlterField(
            model_name='quote',
            name='quote_deadline',
            field=models.DateField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(datetime.date(2020, 5, 20))]),
        ),
        migrations.CreateModel(
            name='QuoteOrderReady',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(default='system', max_length=512)),
                ('updated_by', models.CharField(default='system', max_length=512)),
                ('status', models.IntegerField(choices=[(0, 'Inactive'), (1, 'Active')], default=1)),
                ('total_weight_unit', models.CharField(choices=[('kg', 'KG'), ('tonnes', 'TONS'), ('lbs', 'LBS')], default=None, max_length=255, null=True)),
                ('total_weight', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('total_volume_unit', models.CharField(choices=[('cbm', 'CBM')], default=None, max_length=255, null=True)),
                ('total_volume', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('total_volumetric_weight_unit', models.CharField(choices=[('kg', 'KGS')], default=None, max_length=255, null=True)),
                ('total_volumetric_weight', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('is_order_ready', models.BooleanField(default=False)),
                ('order_ready_date', models.DateField(blank=True, null=True, validators=[utils.helpers.present_or_future_date])),
                ('invoice_value', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('invoice_value_currency', models.CharField(default='INR', max_length=5)),
                ('handover_date', models.DateField(blank=True, null=True, validators=[utils.helpers.present_or_future_date])),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='order_ready_address', to='address.Address')),
                ('quote', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='quote.Quote')),
                ('transport_mode', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='order_ready_transport_mode', to='quote.QuoteTransportMode')),
            ],
            options={
                'db_table': 'quote_order_readies',
            },
            bases=(models.Model, utils.base_models.QuoteChoice, quote.managers.quote_manager.QuoteOrderReadyManager),
        ),
    ]