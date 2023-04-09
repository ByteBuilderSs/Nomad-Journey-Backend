# Generated by Django 4.1.7 on 2023-04-09 06:04

import accounts.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_name', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserInterest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interest_name', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_name', models.CharField(blank=True, max_length=100)),
                ('country', models.CharField(blank=True, max_length=100)),
                ('c_lat', models.FloatField()),
                ('c_long', models.FloatField()),
                ('abbrev_city', models.CharField(blank=True, max_length=3)),
            ],
            options={
                'unique_together': {('city_name', 'country')},
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('User_birthdate', models.DateField(blank=True, null=True)),
                ('User_about_me', models.TextField(blank=True, null=True)),
                ('User_job', models.CharField(blank=True, max_length=100, null=True)),
                ('User_education', models.CharField(blank=True, max_length=100, null=True)),
                ('User_nationality', models.CharField(blank=True, max_length=100, null=True)),
                ('User_address', models.TextField(blank=True, null=True)),
                ('User_address_lat', models.FloatField(blank=True, null=True)),
                ('User_address_long', models.FloatField(blank=True, null=True)),
                ('User_gender', models.CharField(blank=True, choices=[(1, 'Male'), (2, 'Female'), (3, 'Other')], max_length=1, null=True)),
                ('User_country_code', models.CharField(blank=True, max_length=2, null=True)),
                ('User_country', models.CharField(blank=True, max_length=100, null=True)),
                ('User_city', models.CharField(max_length=100)),
                ('User_apt', models.CharField(blank=True, max_length=100, null=True)),
                ('User_postal_code', models.CharField(blank=True, max_length=10, null=True)),
                ('User_phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('profile_photo', models.ImageField(blank=True, null=True, upload_to='customer_photos')),
                ('image_code', models.TextField(blank=True, null=True)),
                ('ssn', models.CharField(blank=True, max_length=20, null=True)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('password_again', models.CharField(max_length=255)),
                ('username', models.CharField(max_length=255, unique=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('hosting_availability', models.CharField(blank=True, choices=[('Accepting Guests', 'Accepting Guests'), ('Maybe Accepting Guests', 'Maybe Accepting Guests'), ('Not Accepting Guests', 'Not Accepting Guests'), ('Wants to Meet Up', 'Wants to Meet Up')], max_length=50, null=True)),
                ('hometown', models.CharField(blank=True, max_length=80, null=True)),
                ('why_Im_on_nomadjourney', models.TextField(blank=True, null=True)),
                ('favorite_music_movie_book', models.TextField(blank=True, null=True)),
                ('amazing_thing_done', models.TextField(blank=True, null=True)),
                ('teach_learn_share', models.TextField(blank=True, null=True)),
                ('what_Ican_share_with_host', models.TextField(blank=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('interests', models.ManyToManyField(blank=True, default=None, to='accounts.userinterest')),
                ('langF', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='langF', to='accounts.language')),
                ('langL', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='langL', to='accounts.language')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', accounts.models.UserManager()),
            ],
        ),
    ]
