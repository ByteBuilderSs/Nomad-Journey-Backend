from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext as _
from utils.models import City, Language, UserInterest


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
    MALE = 1
    FEMALE = 2
    OTHER = 3
    GENDER_CHOICES = (
        (MALE, _('Male')),
        (FEMALE, _('Female')),
        (OTHER , _('Other')))
    HOSTING_AVAILABILITY_CHOICE = ( ('Accepting Guests' , 'Accepting Guests'),
                                    ('Maybe Accepting Guests' , 'Maybe Accepting Guests'),
                                    ('Not Accepting Guests' , 'Not Accepting Guests'),
                                    ('Wants to Meet Up' , 'Wants to Meet Up'))
    User_birthdate = models.DateField(null=True , blank=True)
    User_about_me = models.TextField(null=True , blank=True)
    User_job = models.CharField(max_length=100 , null=True , blank=True)
    User_education = models.CharField(max_length=100,null=True , blank=True)
    User_nationality = models.CharField(max_length=100, null=True,blank=True)
    User_address = models.TextField(blank=True , null=True)
    User_address_lat = models.FloatField(null=True,blank=True)
    User_address_long = models.FloatField(null = True,blank=True)
    User_gender = models.CharField(max_length=1, choices=GENDER_CHOICES , null=True,blank=True)
    User_country_code = models.CharField(max_length=2 , null=True,blank=True)
    User_country = models.CharField(max_length=100 , null=True,blank=True)
    # User_city = models.ForeignKey(City,on_delete=models.CASCADE,default=None  ,null=True,blank=True)
    User_city = models.CharField(max_length=100)
    User_apt = models.CharField(max_length=100, null=True,blank=True)
    User_postal_code = models.CharField(max_length=10 , null=True,blank=True)
    User_phone_number = models.CharField(max_length=20 , null=True,blank=True)
    # is_active = models.BooleanField(default=True)
    profile_photo = models.ImageField(upload_to='customer_photos' , null=True,blank=True)
    image_code = models.TextField(null=True, blank=True)
    ssn = models.CharField(max_length=20 , null=True,blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255 , unique=True)
    password = models.CharField(max_length=255)
    password_again = models.CharField(max_length=255)
    username = models.CharField(max_length=255 , unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    hosting_availability = models.CharField(max_length=50, choices=HOSTING_AVAILABILITY_CHOICE , null=True,blank=True)
    hometown = models.CharField(max_length=80 , null=True , blank=True)
    why_Im_on_nomadjourney = models.TextField(blank=True , null=True)
    favorite_music_movie_book = models.TextField(blank=True , null=True)
    amazing_thing_done = models.TextField(blank=True , null=True)
    teach_learn_share = models.TextField(blank=True , null=True)
    what_Ican_share_with_host = models.TextField(blank=True , null=True)
    interests = models.ManyToManyField(UserInterest ,default=None  ,blank=True )
    langF = models.ForeignKey(Language ,on_delete=models.CASCADE,default=None  ,null=True,blank=True , related_name = 'langF' )
    langL = models.ForeignKey(Language ,on_delete=models.CASCADE,default=None  ,null=True,blank=True , related_name= 'langL' )
    # posts_count = models.IntegerField(default=0)
    # announcements_count = models.IntegerField(default=0)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.first_name+" "+self.last_name
    

