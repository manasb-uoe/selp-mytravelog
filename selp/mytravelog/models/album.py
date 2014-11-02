from django.db import models
from mytravelog.models.user_profile import UserProfile

__author__ = 'Manas'


class Album(models.Model):
    user_profile = models.ForeignKey(UserProfile)
    name = models.CharField(max_length=128, null=False)
    url_name = models.CharField(max_length=128, null=False)
    start_date = models.DateField(max_length=128, null=False)
    end_date = models.DateField(max_length=128, null=False)
    cover_picture = models.ImageField(upload_to='mytravelog/cover_pictures', blank=True, default='/media/mytravelog/cover_pictures/default_cover_picture.png')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_At = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name + ": " + self.user_profile.user.get_full_name()

    class Meta():
        unique_together = ('user_profile', 'name')
        ordering = ['-created_at']


