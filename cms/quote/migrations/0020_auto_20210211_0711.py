# Generated by Django 2.2.5 on 2021-02-11 07:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quote', '0019_auto_20210210_1312'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='quote_status',
            field=models.CharField(choices=[('open', 'open'), ('expired', 'expired'), ('booked', 'booked'), ('cancelled', 'cancelled'), ('pending', 'pending')], default=1, max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='packagedetails',
            name='quote',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='package_details', to='quote.Quote'),
        ),
        migrations.AlterField(
            model_name='quotetransportmode',
            name='quote',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='transport_modes', to='quote.Quote'),
        ),
    ]
