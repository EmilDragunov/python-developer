# Generated by Django 3.2.16 on 2024-09-13 09:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0014_follow_unique_name_follower'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='follow',
            name='unique_name_follower',
        ),
    ]