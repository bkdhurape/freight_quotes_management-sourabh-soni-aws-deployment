# Generated by Django 2.2.7 on 2020-01-02 08:53

import customer.managers.customer_manager
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('company', '0001_initial'),
        ('department', '0001_initial'),
        ('country', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(default='system', max_length=512)),
                ('updated_by', models.CharField(default='system', max_length=512)),
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(default=None, max_length=255, validators=[django.core.validators.MinLengthValidator(4)])),
                ('email', models.EmailField(default=None, error_messages={'required': 'Customer email required..!'}, max_length=254, unique=True)),
                ('secondary_email', models.TextField(default=None, null=True)),
                ('contact_no_dial_code', models.CharField(default=None, max_length=12, null=True)),
                ('contact_no', models.CharField(default=None, max_length=12, null=True, validators=[django.core.validators.MinLengthValidator(10), django.core.validators.RegexValidator(regex='\\d{10}')])),
                ('landline_no_dial_code', models.CharField(default=None, max_length=12, null=True)),
                ('landline_no', models.CharField(default=None, max_length=12, null=True, validators=[django.core.validators.MinLengthValidator(10), django.core.validators.RegexValidator(regex='\\d{10}')])),
                ('customer_type', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('password', models.CharField(default=None, max_length=255, null=True)),
                ('designation', models.CharField(default=None, max_length=25, null=True)),
                ('expertise', models.CharField(default=None, max_length=255, null=True)),
                ('registration_token', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('status', models.IntegerField(choices=[(0, 'Inactive'), (1, 'Active'), (2, 'Signup Pending')], default=1)),
                ('company', models.ManyToManyField(db_table='customer_companies', related_name='customer_companies', to='company.Company')),
                ('department', models.ManyToManyField(db_table='customer_departments', to='department.Department')),
                ('home_company', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='company.Company')),
                ('home_country', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='country.Country')),
                ('supervisor', models.ManyToManyField(blank=True, db_table='customer_supervisors', related_name='customers', to='customer.Customer')),
            ],
            options={
                'db_table': 'customers',
            },
            bases=(models.Model, customer.managers.customer_manager.CustomerManager),
        ),
    ]