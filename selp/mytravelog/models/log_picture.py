from django.db import models
from django.db.models.fields.related import ForeignKey
from mytravelog.models.log import Log

__author__ = 'Manas'


class LogPicture(models.Model):
    log = ForeignKey(Log)
    picture = models.ImageField(upload_to='mytravelog/log_pictures', null=False)

    def __unicode__(self):
        return self.log.city.name + ": " + str(self.id)


# auto delete file when imagefield is deleted
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver

@receiver(post_delete, sender=LogPicture)
def auto_delete_file(sender, instance, **kwargs):
    # Pass false so ImageField doesn't save the model.
    instance.picture.delete(False)