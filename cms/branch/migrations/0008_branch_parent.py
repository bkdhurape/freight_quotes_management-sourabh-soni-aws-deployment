# Generated by Django 2.2.5 on 2020-02-14 06:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0007_auto_20200106_1242'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='branch.Branch'),
        ),
    ]