# Generated by Django 3.1.6 on 2021-04-28 15:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('networkext', '0005_auto_20210428_1555'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='friend',
            new_name='friend_list',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='like',
            new_name='like_list',
        ),
    ]
