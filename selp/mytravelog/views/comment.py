import json

from django.http.response import HttpResponse, Http404

from mytravelog.models.comment import Comment
from mytravelog.models.log import Log
from mytravelog.models.user_profile import UserProfile
from django.contrib.humanize.templatetags.humanize import naturaltime


__author__ = 'Manas'


def create_log_comment(request, log_id):
    """
    Creates a new comment on the log with the provided
    log_id. It also validates the comment body provided
    in the POST request. Also note that this view only
    accepts ajax requests, else a 404 error is raised.
    """
    user = request.user
    return_data = {}
    if request.is_ajax():
        if user.is_authenticated():
            # get user profile of commenter, the log that they commented on and comment body
            log = Log.objects.get_log_by_id(log_id)
            user_profile = UserProfile.objects.get(user=user)
            body = request.POST.get('body', '')
            if len(body) == 0:
                return_data['error'] = 'Comment cannot be left blank'
            elif len(body) > 150:
                return_data['error'] = 'Comment length cannot exceed 150 characters'
            else:
                # create new comment
                comment = Comment()
                comment.log = log
                comment.commenter_user_profile = user_profile
                comment.body = body
                comment.save()

                # send back data required to add a new comment to template
                return_data['username'] = user.username
                return_data['profile_picture_url'] = user_profile.profile_picture.url
                return_data['full_name'] = user.get_full_name()
                return_data['body'] = comment.body
                return_data['created_at'] = naturaltime(comment.created_at)
                return_data['comment_id'] = comment.id
        else:
            return_data['redirect_to'] = "/mytravelog/sign_in/"

        return_data = json.dumps(return_data)
        mimetype = "application/json"
        return HttpResponse(return_data, mimetype)
    else:
        raise Http404


def delete_log_comment(request, comment_id):
    """
    Deletes a comment with the comment id provided. It first
    checks whether the comment actually belongs the current
    user. If this is not that the case, then an error is returned.
    Else, the comment is successfully deleted. Also note that
    this view only accepts ajax requests, else a 404 error is raised.
    """
    user = request.user
    return_data = {}
    if request.is_ajax():
        if user.is_authenticated():
            # get comment associated with the id, and check if it actually belongs to the user deleting it
            comment_to_delete = Comment.objects.get(id=comment_id)
            if comment_to_delete.commenter_user_profile.user == user:
                comment_to_delete.delete()
            else:
                return_data['error'] = "This comment does not belong to you"
        else:
            return_data['redirect_to'] = "/mytravelog/sign_in/"

        return_data = json.dumps(return_data)
        mimetype = "application/json"
        return HttpResponse(return_data, mimetype)
    else:
        raise Http404

