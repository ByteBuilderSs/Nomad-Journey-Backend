# Generated by Django 4.1.7 on 2023-05-23 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_user_coin_to_buy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='coin_to_buy',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='coins',
            field=models.IntegerField(default=5),
        ),
    ]
