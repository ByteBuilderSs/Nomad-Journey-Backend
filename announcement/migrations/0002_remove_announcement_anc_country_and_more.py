# Generated by Django 4.1.7 on 2023-04-04 09:46

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('announcement', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='announcement',
            name='anc_country',
        ),
        migrations.AlterField(
            model_name='announcement',
            name='anc_city',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='announcement',
            name='volunteer_hosts',
            field=models.ManyToManyField(null=True, related_name='hosts_anc', to=settings.AUTH_USER_MODEL),
        ),
    ]
