# Generated by Django 2.2.5 on 2020-04-02 14:49

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import enquiry_management.manager.company_expertise_manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('company', '0007_auto_20200221_0641'),
        ('commodity', '0001_initial'),
        ('country', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyExpertise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(default='system', max_length=512)),
                ('updated_by', models.CharField(default='system', max_length=512)),
                ('status', models.IntegerField(choices=[(0, 'Inactive'), (1, 'Active')], default=1)),
                ('transport_mode', models.CharField(choices=[('AI', 'Air-Import'), ('AE', 'Air-Export'), ('ATC', 'Air-Third Country'), ('ACI', 'Air-Courier Import'), ('ACE', 'Air-Courier Export'), ('ACTC', 'Air-Courier Third Country'), ('FCLI', 'FCL-Import'), ('FCLE', 'FCL-Export'), ('FCLTC', 'FCL-Third Country'), ('LCLI', 'LCL-Import'), ('LCLE', 'LCL-Export'), ('LCLTC', 'LCL-Third Country')], default=None, max_length=255)),
                ('container_type', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), blank=True, null=True, size=None)),
                ('hazardous', models.BooleanField(default=True)),
                ('instant_quotes', models.BooleanField(default=True)),
                ('temperature_controlled', models.BooleanField(default=True, null=True)),
                ('commodity', models.ManyToManyField(db_table='company_expertise_commodities', to='commodity.Commodity')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='company.Company')),
                ('from_trade_lanes', models.ManyToManyField(blank=True, related_name='company_expertise_from_trade_lanes', to='country.Country')),
                ('to_trade_lanes', models.ManyToManyField(blank=True, related_name='company_expertise_to_trade_lanes', to='country.Country')),
                ('trade_lanes', models.ManyToManyField(blank=True, related_name='company_expertise_trade_lanes', to='country.Country')),
            ],
            options={
                'unique_together': {('company', 'transport_mode')},
                'db_table': 'company_experties',
            },
            bases=(models.Model, enquiry_management.manager.company_expertise_manager.CompanyExpertiseManager),
        ),
    ]