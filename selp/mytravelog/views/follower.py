import json
from django.http.response import HttpResponse, Http404
from mytravelog.models.follower import Follower
from mytravelog.models.user_profile import UserProfile

__author__ = 'Manas'


def create_follower(request, following_user_profile_id):
    user = request.user
    return_data = {}
    if request.is_ajax():
        if user.is_authenticated():
            # get follower and following user profile
            follower_user_profile = UserProfile.objects.get(user=user)
            following_user_profile = UserProfile.objects.get(id=following_user_profile_id)

            # create new follower only if it does not already exist AND the user is not trying to follow themselves
            existing_follower = Follower.objects.get_follower(follower_user_profile, following_user_profile)
            if existing_follower is None:
                if follower_user_profile != following_user_profile:
                    new_follower = Follower()
                    new_follower.follower_user_profile = follower_user_profile
                    new_follower.following_user_profile = following_user_profile
                    new_follower.save()
                else:
                    return_data['error'] = "You cannot follow yourself"
        else:
            return_data['redirect_to'] = "/mytravelog/sign_in/"

        return_data = json.dumps(return_data)
        mimetype = "application/json"
        return HttpResponse(return_data, mimetype)
    else:
        raise Http404


def delete_follower(request, following_user_profile_id):
    user = request.user
    return_data = {}
    if request.is_ajax():
        if user.is_authenticated():
            # get follower and following user profile
            follower_user_profile = UserProfile.objects.get(user=user)
            following_user_profile = UserProfile.objects.get(id=following_user_profile_id)

            # delete follower if it exists
            follower_to_delete = Follower.objects.get_follower(follower_user_profile, following_user_profile)
            if follower_to_delete is not None:
                follower_to_delete.delete()
        else:
            return_data['redirect_to'] = "/mytravelog/sign_in/"

        return_data = json.dumps(return_data)
        mimetype = "application/json"
        return HttpResponse(return_data, mimetype)
    else:
        raise Http404