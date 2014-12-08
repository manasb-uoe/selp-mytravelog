from django.db import models
from mytravelog.models.user_profile import UserProfile

__author__ = 'Manas'


class FollowerManager(models.Manager):

    def get_requested_user_followers(self, requested_user_profile, current_user_profile):
        requested_user_followers = self.filter(following_user_profile=requested_user_profile)
        for follower in requested_user_followers:
            follower.is_followed = False
            if current_user_profile is not None:
                if len(self.filter(follower_user_profile=current_user_profile,
                                   following_user_profile=follower.follower_user_profile)) > 0:
                    follower.is_followed = True
                if follower.follower_user_profile != current_user_profile:
                    follower.can_follow = True
                else:
                    follower.can_follow = False
        return requested_user_followers

    def get_requested_user_following(self, requested_user_profile, current_user_profile):
        requested_user_following = self.filter(follower_user_profile=requested_user_profile)
        if current_user_profile is not None:
            for following in requested_user_following:
                following.is_followed = True
                if following.following_user_profile != current_user_profile:
                    following.can_follow = True
                else:
                    following.can_follow = False
        return requested_user_following

    def is_requested_user_followed_by_current_user(self, requested_user_profile, current_user_profile):
        is_followed = False
        if current_user_profile is not None:
            if len(self.filter(follower_user_profile=current_user_profile,
                               following_user_profile=requested_user_profile)) > 0:
                is_followed = True
        return is_followed

    def get_follower_count(self, user_profile):
        return self.filter(following_user_profile=user_profile).count()

    def get_follower(self, follower_user_profile, following_user_profile):
        try:
            follower = self.get(follower_user_profile=follower_user_profile,
                                following_user_profile=following_user_profile)
        except Follower.DoesNotExist:
            follower = None
        return follower


class Follower(models.Model):

    # Relations
    follower_user_profile = models.ForeignKey(UserProfile, related_name="follower_user_profile")
    following_user_profile = models.ForeignKey(UserProfile, related_name="following_user_profile")

    # Managers
    objects = FollowerManager()

    def __unicode__(self):
        return str(self.id) + " " + self.following_user_profile.user.get_full_name()
