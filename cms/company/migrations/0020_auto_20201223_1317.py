# Generated by Django 2.2.5 on 2020-12-23 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0019_company_company_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='cin_document',
            field=models.FileField(blank=True, null=True, upload_to='company/document/cin/% Y/% m/% d/'),
        ),
        migrations.AddField(
            model_name='company',
            name='gst_document',
            field=models.FileField(blank=True, null=True, upload_to='company/document/gst/% Y/% m/% d/'),
        ),
        migrations.AddField(
            model_name='company',
            name='iec_document',
            field=models.FileField(blank=True, null=True, upload_to='company/document/iec/% Y/% m/% d/'),
        ),
        migrations.AddField(
            model_name='company',
            name='pan_document',
            field=models.FileField(blank=True, null=True, upload_to='company/document/pan/% Y/% m/% d/'),
        ),
    ]
