# Generated by Django 3.1.6 on 2021-03-03 18:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_auto_20210303_1823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchlist',
            name='watcher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watchlists_w', to=settings.AUTH_USER_MODEL, unique=True),
        ),
    ]
