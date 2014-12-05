__author__ = 'Manas'

from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    rank = models.IntegerField(max_length=10, null=False, default=-1)
    profile_picture = models.ImageField(upload_to='mytravelog/profile_pictures', blank=True, default='/media/mytravelog/profile_pictures/default_profile_picture.png')
    cover_picture = models.ImageField(upload_to='mytravelog/cover_pictures', blank=True, default='/media/mytravelog/cover_pictures/default_cover_picture.png')

    def __unicode__(self):
        return self.user.username