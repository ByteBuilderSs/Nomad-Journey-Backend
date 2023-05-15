# Generated by Django 4.1.7 on 2023-05-04 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='image_code',
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_photo',
            field=models.ImageField(blank=True, null=True, upload_to='img_profile'),
        ),
    ]