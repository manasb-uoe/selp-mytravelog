from django.db import models
from django.db.models.fields.related import ForeignKey
from mytravelog.models.log import Log

__author__ = 'Manas'


class LogPicture(models.Model):
    log = ForeignKey(Log)
    picture = models.ImageField(upload_to='mytravelog/log_pictures', null=False)

    def __unicode__(self):
        return self.log.city.name + ": " + str(self.id)