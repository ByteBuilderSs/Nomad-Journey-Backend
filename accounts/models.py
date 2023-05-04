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
    # User_country = models.CharField(max_length=100 , null=True,blank=True)
    User_city = models.ForeignKey(City,on_delete=models.CASCADE,default=None  ,null=True,blank=True)
    # User_city = models.CharField(max_length=100)
    User_apt = models.CharField(max_length=100, null=True,blank=True)
    User_postal_code = models.CharField(max_length=10 , null=True,blank=True)
    User_phone_number = models.CharField(max_length=20 , null=True,blank=True)
    # is_active = models.BooleanField(default=True)

    # start
    profile_photo = models.ImageField(upload_to='img_profile', null=True, blank=True)
    # end

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
    interests = models.ManyToManyField(UserInterest ,default=None,blank=True)
    langF = models.ManyToManyField(Language ,default=None  ,blank=True , related_name = 'langF' )
    langL = models.ManyToManyField(Language ,default=None  ,blank=True , related_name= 'langL' )

    is_sun = models.BooleanField(default=False)
    is_sat = models.BooleanField(default=False)
    is_mon = models.BooleanField(default=False)
    is_tue = models.BooleanField(default=False)
    is_wed = models.BooleanField(default=False)
    is_thu = models.BooleanField(default=False)
    is_fri = models.BooleanField(default=False)
    ONE_TR = 1
    TWO_TR = 2
    THREE_TR = 3
    FOUR_TR = 4
    FIVE_TR = 5
    SIX_TR = 6
    SEVENT_TR = 7
    EIGHT_TR = 8
    NINE_TR = 9
    TEN_TR = 10
    ELEVEN_TR = 11
    TWELVE_TR = 12
    THIRTEEN_TR = 13
    FOURTEEN_TR = 14
    FIFTEEN_TR = 15
    maximum_number_of_guests = (
        (ONE_TR, _('1')),
        (TWO_TR, _('2')),
        (THREE_TR, _('3')),
        (FOUR_TR, _('4')),
        (FIVE_TR, _('5')),
        (SIX_TR, _('6')),
        (SEVENT_TR, _('7')),
        (EIGHT_TR, _('8')),
        (NINE_TR, _('9')),
        (TEN_TR, _('10')),
        (ELEVEN_TR, _('11')),
        (TWELVE_TR, _('12')),
        (THIRTEEN_TR, _('13')),
        (FOURTEEN_TR, _('14')),
        (FIFTEEN_TR, _('15'))
    )
    ANY = 1
    MALE = 2
    FEMALE = 3
    prefered_gender_to_host = (
        (ANY, _('Any')),
        (MALE, _('Male')),
        (FEMALE , _('Female')))
    is_pet_friendly = models.BooleanField(null=True , blank=True)
    is_kid_friendly = models.BooleanField(null=True , blank=True)
    is_smoking_allowed = models.BooleanField(null=True , blank=True)
    SHARED_BED= 1
    SHARED_ROOM = 2
    PRIVATE_ROOM = 3
    PUBLIC_ROOM = 4
    sleeping_arrangments = (
        (SHARED_BED, _('shared_bed')),
        (SHARED_ROOM, _('shared_room')),
        (PRIVATE_ROOM , _('private_room')),
        (PUBLIC_ROOM , _('public_room')))
    description_of_sleeping_arrangement = models.TextField(max_length=3000 , null=True , blank=True)
    roommate_situation = models.TextField(max_length=3000 , null=True , blank=True)
    additional_information = models.TextField(max_length=3000 ,null=True , blank=True)
    i_have_pet = models.BooleanField(null=True , blank=True)
    kids_at_home = models.BooleanField(null=True , blank=True)
    smoking_at_home = models.BooleanField(null=True , blank=True)
    wheelchair_accessible = models.BooleanField(null=True , blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.first_name+" "+self.last_name
    

