__author__ = 'Manas'

from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    city_count = models.IntegerField(max_length=10, null=False, default=0)
    country_count = models.IntegerField(max_length=10, null=False, default=0)
    log_count = models.IntegerField(max_length=10, null=False, default=0)
    total_score = models.IntegerField(max_length=50, null=False, default=0)
    profile_picture = models.ImageField(upload_to='mytravelog/profile_pictures', blank=True, default='/media/mytravelog/profile_pictures/default_profile_picture.png')

    def __unicode__(self):
        return self.user.username