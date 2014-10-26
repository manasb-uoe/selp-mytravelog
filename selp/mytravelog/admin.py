from django.contrib import admin
from mytravelog.models import city, user_profile


# Register your models here.
admin.site.register(city.City)
admin.site.register(user_profile.UserProfile)