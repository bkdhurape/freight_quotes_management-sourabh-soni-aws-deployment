# Generated by Django 2.2.5 on 2020-03-12 10:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0007_auto_20200221_0641'),
        ('currency', '0002_auto_20200122_1038'),
    ]

    operations = [
        migrations.AddField(
            model_name='currencyprofile',
            name='company',
            field=models.ForeignKey(default=4, on_delete=django.db.models.deletion.DO_NOTHING, to='company.Company'),
            preserve_default=False,
        ),
    ]
