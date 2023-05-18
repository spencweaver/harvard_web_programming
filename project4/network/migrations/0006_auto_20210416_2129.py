# Generated by Django 3.1.6 on 2021-04-16 21:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_auto_20210414_2057'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useruser',
            name='follower',
        ),
        migrations.AddField(
            model_name='useruser',
            name='follower',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='followers', to='network.user'),
            preserve_default=False,
        ),
    ]
