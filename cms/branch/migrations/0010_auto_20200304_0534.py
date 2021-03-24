# Generated by Django 2.2.5 on 2020-03-04 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('country', '0001_initial'),
        ('branch', '0009_branch_is_head_branch'),
    ]

    operations = [
        migrations.AddField(
            model_name='branchtransportmode',
            name='from_trade_lanes',
            field=models.ManyToManyField(blank=True, related_name='branch_transport_from_trade_lanes', to='country.Country'),
        ),
        migrations.AddField(
            model_name='branchtransportmode',
            name='to_trade_lanes',
            field=models.ManyToManyField(blank=True, related_name='branch_transport_to_trade_lanes', to='country.Country'),
        ),
        migrations.AlterField(
            model_name='branchtransportmode',
            name='trade_lanes',
            field=models.ManyToManyField(blank=True, related_name='branch_transport_trade_lanes', to='country.Country'),
        ),
        migrations.AlterField(
            model_name='branchtransportmode',
            name='transport_mode',
            field=models.CharField(choices=[('AI', 'Air-Import'), ('AE', 'Air-Export'), ('ATC', 'Air-Third Country'), ('FCLI', 'FCL-Import'), ('FCLE', 'FCL-Export'), ('FCLTC', 'FCL-Third Country'), ('LCLI', 'LCL-Import'), ('LCLE', 'LCL-Export'), ('LCLTC', 'LCL-Third Country')], default=None, max_length=255),
        ),
    ]