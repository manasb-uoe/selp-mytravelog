from django.db.models.fields.related import ForeignKey
from django.db import models

from mytravelog.models.log import Log
from mytravelog.models.user_profile import UserProfile


__author__ = 'Manas'


class Comment(models.Model):
    log = ForeignKey(Log)
    commenter_user_profile = ForeignKey(UserProfile)
    body = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return str(self.log.id) + " " + self.commenter_user_profile.user.get_full_name()

    class Meta():
        ordering = ['created_at']