from django.contrib import admin
from .models import User , City , UserInterest , Language
# Register your models here.

admin.site.register(User)
admin.site.register(City)
admin.site.register(Language)
admin.site.register(UserInterest)