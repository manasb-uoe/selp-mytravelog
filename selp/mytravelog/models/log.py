from django.db import models
from django.db.models.fields.related import ForeignKey

from mytravelog.models.album import Album
from mytravelog.models.city import City
from mytravelog.models.user_profile import UserProfile


__author__ = 'Manas'


class LogManager(models.Manager):

    def get_user_logs(self, requested_user_profile):
        return self.filter(user_profile=requested_user_profile)

    def get_city_logs(self, requested_city):
        return self.filter(city=requested_city)

    def get_album_logs(self, requested_album):
        return self.filter(album=requested_album)

    def get_log_by_id(self, log_id):
        try:
            log = self.get(id=log_id)
        except Log.DoesNotExist:
            log = None
        return log

    def get_users_logs(self, user_profiles):
        return self.filter(user_profile__in=user_profiles)

    @staticmethod
    def attach_additional_info_to_logs(requested_user_logs, current_user_profile):
        from mytravelog.models.log_picture import LogPicture
        from mytravelog.models.like import Like
        from mytravelog.models.comment import Comment

        for log in requested_user_logs:
            # attach pictures
            log_pictures = LogPicture.objects.filter(log=log)
            log.pictures = log_pictures
            # attach likes and check if current user liked a log or not
            likes = Like.objects.filter(log=log)
            log.likes = likes
            log.liked = False
            for like in likes:
                if current_user_profile is not None:
                    if like.liker_user_profile == current_user_profile:
                        log.liked = True
            # attach comments and check if current user can delete it or not
            comments = Comment.objects.filter(log=log)
            log.comments = comments
            for comment in comments:
                comment.can_delete = False
                if current_user_profile is not None:
                    if comment.commenter_user_profile == current_user_profile:
                        comment.can_delete = True
            # attach edit permission
            if log.user_profile == current_user_profile:
                log.can_edit = True
            else:
                log.can_edit = False
        return requested_user_logs


class Log(models.Model):

    # Relations
    user_profile = ForeignKey(UserProfile)
    album = ForeignKey(Album, null=True, blank=True)
    city = ForeignKey(City)

    # Attributes
    latitude = models.DecimalField(max_digits=7, decimal_places=4, null=False)
    longitude = models.DecimalField(max_digits=7, decimal_places=4, null=False)
    description = models.CharField(max_length=1000, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    score = models.DecimalField(max_digits=100, decimal_places=7, null=False)

    # Managers
    objects = LogManager()

    def __unicode__(self):
        return self.city.name + ": " + self.user_profile.user.get_full_name()

    class Meta():
        ordering = ['-created_at']