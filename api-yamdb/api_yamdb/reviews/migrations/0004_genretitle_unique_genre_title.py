# Generated by Django 3.2 on 2024-10-09 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_delete_user'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='genretitle',
            constraint=models.UniqueConstraint(fields=('genre', 'title'), name='unique_genre_title'),
        ),
    ]
