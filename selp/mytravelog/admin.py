from django.contrib import admin
from mytravelog.models import city, user_profile, album, log, log_picture, like, comment, follower


# Register your models here.
admin.site.register(city.City)
admin.site.register(user_profile.UserProfile)
admin.site.register(album.Album)
admin.site.register(log.Log)
admin.site.register(log_picture.LogPicture)
admin.site.register(like.Like)
admin.site.register(comment.Comment)
admin.site.register(follower.Follower)