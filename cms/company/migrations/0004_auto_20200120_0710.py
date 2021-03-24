# Generated by Django 2.2.5 on 2020-01-20 07:10

import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0003_merge_20200117_0710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='industry',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('consumer_goods_or_fmcg', 'Consumer Goods/FMCG'), ('engineering_and_manufacturing', 'Engineering and Manufacturing'), ('textiles_and_fashion_apparel', 'Textiles and Fashion Apparel'), ('retail', 'Retail'), ('automotive', 'Automotive'), ('electronics', 'Electronics'), ('chemicals', 'Chemicals'), ('healthcare', 'Healthcare'), ('technology', 'Technology'), ('hospitality', 'Hospitality'), ('food_and_beverages', 'Food & Beverages'), ('jewellery', 'Jewellery'), ('renewable_energy_gas_solar_etc', 'Renewable Energy: Gas,Solar etc.'), ('oil_and_gas', 'Oil & Gas'), ('marine', 'Marine'), ('aerospace', 'Aerospace'), ('government_or_defense', 'Government / Defense'), ('other', 'Other')], max_length=255), size=None),
        ),
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(max_length=512, unique=True, validators=[django.core.validators.RegexValidator(regex='^[a-zA-Z\\w]+$')]),
        ),
    ]
