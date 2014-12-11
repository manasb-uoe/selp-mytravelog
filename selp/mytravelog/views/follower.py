import json
from django.http.response import HttpResponse, Http404
from mytravelog.models.follower import Follower
from mytravelog.models.user_profile import UserProfile

__author__ = 'Manas'


def create_follower(request, following_user_profile_id):
    """
    Creates a new follower instance with follower being the
    current user, and the user being followed is queried using
    the provided following_user_following_user_profile_id. It also
    checks if the current user is trying to follow themselves. If
    this is the case, then an error is returned. Else, a follower
    is created successfully. Also note that this view only accepts
    ajax requests, else a 404 error is raised.
    """
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
    """
    Deleted a follower instance with follower being the
    current user, and the user being followed is queried using
    the provided following_user_following_user_profile_id.
    Also note that this view only accepts ajax requests,
    else a 404 error is raised.
    """
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