# Generated by Django 2.2.5 on 2020-08-27 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0020_auto_20200826_1450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_type',
            field=models.CharField(choices=[('importer_or_exporter', 'Importer/Exporter'), ('freight_agent', 'Freight Agent'), ('customs_agent', 'Customs Agent'), ('e-commerce_platform', 'E-Commerce Platform'), ('transporter', 'Transporter'), ('other', 'Other')], max_length=20),
        ),
    ]
