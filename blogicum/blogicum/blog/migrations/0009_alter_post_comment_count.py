# Generated by Django 3.2.16 on 2024-07-12 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20240711_2251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='comment_count',
            field=models.IntegerField(blank=True, default=0, verbose_name='Количество комментариев'),
        ),
    ]
