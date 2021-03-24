# Generated by Django 2.2.5 on 2020-04-03 11:50

import customer.managers.invited_service_manager
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0004_auto_20200324_0723'),
        ('company', '0007_auto_20200221_0641'),
        ('customer', '0012_auto_20200330_0733'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='client',
            field=models.ManyToManyField(blank=True, db_table='customer_clients', related_name='customer_clients', to='company.Company'),
        ),
        migrations.AddField(
            model_name='customer',
            name='is_super_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='InvitedVendor',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(default='system', max_length=512)),
                ('updated_by', models.CharField(default='system', max_length=512)),
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(default=None, max_length=255, validators=[django.core.validators.MinLengthValidator(4), django.core.validators.RegexValidator(regex='^[A-Za-z]+[A-Za-z\\d\\._\\s]+$')])),
                ('email', models.EmailField(default=None, error_messages={'required': 'Vendor email required..!'}, max_length=254, unique=True)),
                ('contact_no', models.CharField(blank=True, default=None, max_length=12, null=True, validators=[django.core.validators.MinLengthValidator(10), django.core.validators.RegexValidator(regex='\\d{10}')])),
                ('landline_no_dial_code', models.CharField(blank=True, default=None, max_length=12, null=True)),
                ('landline_no', models.CharField(blank=True, default=None, max_length=12, null=True, validators=[django.core.validators.MinLengthValidator(10), django.core.validators.RegexValidator(regex='\\d{10}')])),
                ('company_name', models.CharField(max_length=512, validators=[django.core.validators.MinLengthValidator(4), django.core.validators.RegexValidator(regex='^[a-zA-Z\\w]+$')])),
                ('status', models.IntegerField(choices=[(0, 'Reject'), (1, 'Active'), (2, 'Pending')], default=2)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='customer.Customer')),
                ('customer_company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='customer_company', to='company.Company')),
                ('vendor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='vendor.Vendor')),
                ('vendor_company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='company.Company')),
            ],
            options={
                'db_table': 'invited_vendors',
            },
            bases=(models.Model, customer.managers.invited_service_manager.InvitedVendorManager),
        ),
    ]
