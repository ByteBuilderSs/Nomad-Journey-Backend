# Generated by Django 4.1.7 on 2023-04-06 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_user_announcements_count_user_posts_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='announcements_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='posts_count',
            field=models.IntegerField(default=0),
        ),
    ]
