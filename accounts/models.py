from django.db import models
from django.contrib.auth.models import AbstractUser , BaseUserManager
# Create your models here.

class UserManager(BaseUserManager):
    use_in_migrations = True
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff' , True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),)
    birthdate = models.DateField(null=True)
    about_me = models.TextField(null=True)
    job = models.CharField(max_length=100 , null=True)
    education = models.CharField(max_length=100,null=True)
    nationality = models.CharField(max_length=100, null=True)
    address = models.TextField(blank=True , null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES , null=True)
    country_code = models.CharField(max_length=2 , null=True)
    country = models.CharField(max_length=100 , null=True)
    city = models.CharField(max_length=100 , null=True)
    postal_code = models.CharField(max_length=10 , null=True)
    phone_number = models.CharField(max_length=20 , null=True)
    # is_active = models.BooleanField(default=True)
    profile_photo = models.ImageField(upload_to='customer_photos' , null=True)
    ssn = models.CharField(max_length=20 , null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255 , unique=True)
    password = models.CharField(max_length=255)
    username = models.CharField(max_length=255 , unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.first_name+" "+self.last_name
