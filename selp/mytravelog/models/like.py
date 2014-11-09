from django.db import models
from django.db.models.fields.related import ForeignKey
from mytravelog.models.log import Log
from mytravelog.models.user_profile import UserProfile

__author__ = 'Manas'


class Like(models.Model):
    log = ForeignKey(Log)
    liker_user_profile = ForeignKey(UserProfile)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return str(self.log.id) + " " + self.user_profile.full_name

    class Meta():
        ordering = ['-created_at']