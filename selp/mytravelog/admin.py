from django.contrib import admin
from mytravelog.models import city, user_profile, album


# Register your models here.
admin.site.register(city.City)
admin.site.register(user_profile.UserProfile)
admin.site.register(album.Album)