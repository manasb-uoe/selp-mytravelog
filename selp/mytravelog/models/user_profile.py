from django.db.models.query_utils import Q

__author__ = 'Manas'

from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    city_count = models.IntegerField(max_length=10, null=False, default=0)
    country_count = models.IntegerField(max_length=10, null=False, default=0)
    rank = models.IntegerField(max_length=10, null=False, default=-1)
    profile_picture = models.ImageField(upload_to='mytravelog/profile_pictures', blank=True, default='/media/mytravelog/profile_pictures/default_profile_picture.png')
    cover_picture = models.ImageField(upload_to='mytravelog/cover_pictures', blank=True, default='/media/mytravelog/cover_pictures/default_cover_picture.png')

    def __unicode__(self):
        return self.user.username

    def update_user_travel_stats(self):
        # imported inside method to prevent circular dependencies
        from mytravelog.models.log import Log

        city_set = set()
        country_set = set()
        all_user_logs = Log.objects.get_user_logs(self)
        for log in all_user_logs:
            city_set.add(log.city.id)
            country_set.add(log.city.country_name)
        self.city_count = len(city_set)
        self.country_count = len(country_set)
        self.save()

    def compute_and_get_user_score(self):
        # imported inside method to prevent circular dependencies
        from mytravelog.models.log import Log
        from mytravelog.models.comment import Comment
        from mytravelog.models.like import Like
        from mytravelog.models.follower import Follower

        # get all user logs
        all_logs = Log.objects.get_user_logs(self)
        log_count = len(all_logs)

        city_set = set()
        country_set = set()
        like_count = 0
        comment_count = 0
        for log in all_logs:
            # get unique cities and countries visited
            city_set.add(log.city)
            country_set.add(log.city.country_name)

            # count non-self likes
            like_count += Like.objects.filter(Q(log=log) & ~Q(liker_user_profile=self)).count()

            # count non-self comments
            comment_count += Comment.objects.filter(Q(log=log) & ~Q(commenter_user_profile=self)).count()

        # get sum of a visited city ranks
        sum_city_ranks = 0
        for city in city_set:
            sum_city_ranks += city.rank

        # get a count of followers
        follower_count = Follower.objects.get_follower_count(self)

        # finally, compute user score
        score = sum_city_ranks + 2*log_count + 0.5*comment_count + 0.5*like_count + follower_count
        return round(score, 5)