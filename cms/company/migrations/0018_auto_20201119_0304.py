# Generated by Django 2.2.5 on 2020-11-19 03:04

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0017_auto_20201027_1124'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='type',
            new_name='user_type',
        ),
        migrations.AlterField(
            model_name='company',
            name='business_activity',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('manufacturer', 'Manufacturer'), ('supplier', 'Supplier'), ('retailer', 'Retailer'), ('wholesaler', 'Wholesaler'), ('distributor', 'Distributor'), ('trader', 'Trader'), ('service', 'Service'), ('agriculture', 'Agriculture'), ('other', 'Other')], max_length=255), blank=True, default=list, size=None),
        ),
        migrations.AlterField(
            model_name='company',
            name='industry',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('consumer_goods_or_fmcg', 'Consumer Goods/FMCG'), ('engineering_and_manufacturing', 'Engineering and Manufacturing'), ('textiles_and_fashion_apparel', 'Textiles and Fashion Apparel'), ('retail', 'Retail'), ('automotive', 'Automotive'), ('electronics', 'Electronics'), ('chemicals', 'Chemicals'), ('healthcare', 'Healthcare'), ('technology', 'Technology'), ('hospitality', 'Hospitality'), ('food_and_beverages', 'Food & Beverages'), ('jewellery', 'Jewellery'), ('renewable_energy_gas_solar_etc', 'Renewable Energy: Gas,Solar etc.'), ('oil_and_gas', 'Oil & Gas'), ('marine', 'Marine'), ('aerospace', 'Aerospace'), ('government_or_defense', 'Government / Defense'), ('other', 'Other')], max_length=255), blank=True, default=list, null=True, size=None),
        ),
        migrations.AlterUniqueTogether(
            name='company',
            unique_together={('name', 'user_type')},
        ),
    ]
