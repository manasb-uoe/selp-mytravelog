import os
import django

__author__ = 'Manas'

if __name__ == "__main__":
    # setup django environment
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "selp.settings")

    from mytravelog.models.user_profile import UserProfile
    django.setup()

    # get all user profiles and score them one by one
    all_user_profiles = UserProfile.objects.all()
    for user_profile in all_user_profiles:
        user_profile.score = user_profile.compute_and_get_user_score()

    # now, sort the user profiles by descending order of score and rank each user
    rank = 1
    all_user_profiles = sorted(all_user_profiles, key=lambda x: x.score, reverse=True)
    for user_profile in all_user_profiles:
        user_profile.rank = rank
        user_profile.save()
        rank += 1

    print "End of user ranking script."