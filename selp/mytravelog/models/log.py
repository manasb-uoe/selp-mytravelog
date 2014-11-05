from django.db import models
from django.db.models.fields.related import ForeignKey
from mytravelog.models.album import Album
from mytravelog.models.city import City
from mytravelog.models.user_profile import UserProfile

__author__ = 'Manas'


class Log(models.Model):
    user_profile = ForeignKey(UserProfile)
    album = ForeignKey(Album, null=True, blank=True)
    city = ForeignKey(City)
    description = models.CharField(max_length=1000, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.city.name + ": " + self.user_profile.user.get_full_name()

    class Meta():
        ordering = ['-created_at']