from django.db import models


class City(models.Model):
    city_name = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    c_lat = models.FloatField()
    c_long = models.FloatField()
    city_image64 = models.TextField(null=True, blank=True)
    abbrev_city = models.CharField(max_length=3, blank=True)
    area = models.TextField(null=True,blank=True)
    population = models.TextField(null=True , blank=True)
    currency = models.TextField(null=True , blank=True)
    explore_more = models.TextField(null=True , blank=True)

    class Meta:
        unique_together = ('city_name', 'country')

    def __str__(self):
        return f'{self.city_name}: ({self.c_lat}, {self.c_long})'

class Language(models.Model):
    language_name = models.CharField(max_length=100, null=True, blank=True , unique=True)

    def __str__(self):
        return self.language_name

class UserInterest(models.Model):
    interest_name = models.CharField(max_length=100, null=True, blank=True , unique=True)

    def __str__(self):
        return self.interest_name