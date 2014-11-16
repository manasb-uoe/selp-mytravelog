from django.db import models
from mytravelog.models.user_profile import UserProfile

__author__ = 'Manas'


class Follower(models.Model):
    follower_user_profile = models.ForeignKey(UserProfile, related_name="follower_user_profile")
    following_user_profile = models.ForeignKey(UserProfile, related_name="following_user_profile")

    def __unicode__(self):
        return str(self.id) + " " + self.following_user_profile.user.get_full_name()