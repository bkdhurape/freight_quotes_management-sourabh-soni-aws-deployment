# Generated by Django 2.2.5 on 2020-09-04 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0010_auto_20200825_1233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companylogisticinfo',
            name='annaul_logistic_spend_currency',
            field=models.CharField(choices=[('INR', 'INR'), ('USD', 'USD'), ('PES', 'PES'), ('AUS', 'AUS'), ('LKR', 'LKR')], max_length=5),
        ),
        migrations.AlterField(
            model_name='companylogisticinfo',
            name='annual_revenue_currency',
            field=models.CharField(choices=[('INR', 'INR'), ('USD', 'USD'), ('PES', 'PES'), ('AUS', 'AUS'), ('LKR', 'LKR')], max_length=5),
        ),
    ]
