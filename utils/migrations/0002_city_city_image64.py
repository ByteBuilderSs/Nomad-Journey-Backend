# Generated by Django 4.1.7 on 2023-05-17 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='city_image64',
            field=models.TextField(blank=True, null=True),
        ),
    ]
