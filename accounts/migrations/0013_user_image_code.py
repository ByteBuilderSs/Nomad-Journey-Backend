# Generated by Django 4.1.7 on 2023-03-22 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0012_user_password_again"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="image_code",
            field=models.TextField(blank=True, null=True),
        ),
    ]