# Generated by Django 3.1.6 on 2021-02-26 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auto_20210226_1513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='is_active',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='title',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
