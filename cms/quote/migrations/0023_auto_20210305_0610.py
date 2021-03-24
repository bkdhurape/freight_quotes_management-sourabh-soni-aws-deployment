# Generated by Django 2.2.5 on 2021-03-05 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quote', '0022_quote_shipment_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='shipment_type',
            field=models.CharField(choices=[('import', 'import'), ('export', 'export'), ('third-country', 'third_country')], default='import', max_length=20),
        ),
    ]