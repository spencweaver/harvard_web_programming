# Generated by Django 3.1.6 on 2021-04-28 15:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('networkext', '0004_user_friend'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='likes',
            new_name='like',
        ),
    ]
