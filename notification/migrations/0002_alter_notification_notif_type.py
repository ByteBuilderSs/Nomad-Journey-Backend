# Generated by Django 4.1.7 on 2023-07-03 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notif_type',
            field=models.CharField(choices=[('like_post', 'like_post'), ('offer_to_host', 'offer_to_host'), ('chosen_as_main_host', 'chosen_as_main_host')], default=None, max_length=200),
        ),
    ]
