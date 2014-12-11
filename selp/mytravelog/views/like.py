import json
from django.http.response import HttpResponse, Http404
from mytravelog.models.like import Like
from mytravelog.models.log import Log
from mytravelog.models.user_profile import UserProfile

__author__ = 'Manas'


def like_log(request, log_id):
    """
    Creates a new like for the log with the provided id. It first checks
    if a like with the same user and log_id already exists. If not, then
    a like is created, else, nothing is created. Also note that this view
    only accepts ajax requests, else a 404 error is raised.
    """
    user = request.user
    return_data = {}
    if request.is_ajax():
        if user.is_authenticated():
            # get user profile of liker and the log that they liked
            log = Log.objects.get_log_by_id(log_id)
            user_profile = UserProfile.objects.get(user=user)

            # create new like only if it does not already exist
            if len(Like.objects.filter(log=log, liker_user_profile=user_profile)) == 0:
                new_like = Like()
                new_like.log = log
                new_like.liker_user_profile = user_profile
                new_like.save()

            # send back data required to add a new like to template
            return_data['username'] = user.username
            return_data['profile_picture_url'] = user_profile.profile_picture.url
        else:
            return_data['redirect_to'] = "/mytravelog/sign_in/"

        return_data = json.dumps(return_data)
        mimetype = "application/json"
        return HttpResponse(return_data, mimetype)
    else:
        raise Http404


def dislike_log(request, log_id):
    """
    Deletes a like for the log with the provided id. It first checks
    if a like with the same user and log_id exists. If not, then
    nothing is deleted, else, the like is deleted successfully. Also
    note that this view only accepts ajax requests, else a 404 error
    is raised.
    """
    user = request.user
    return_data = {}
    if request.is_ajax():
        if user.is_authenticated():
            # get user profile of disliker and the log that they disliked
            log = Log.objects.get_log_by_id(log_id)
            user_profile = UserProfile.objects.get(user=user)

            # delete like if it exists
            like_to_delete = Like.objects.filter(log=log, liker_user_profile=user_profile)
            if len(like_to_delete) != 0:
                like_to_delete.delete()

            # send back data required to remove like from template
            return_data['username'] = user.username
        else:
            return_data['redirect_to'] = "/mytravelog/sign_in/"

        return_data = json.dumps(return_data)
        mimetype = "application/json"
        return HttpResponse(return_data, mimetype)
    else:
        raise Http404