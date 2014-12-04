import json
import datetime
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.query_utils import Q
from django.http.response import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
import math
from mytravelog.models.album import Album
from mytravelog.models.city import City
from mytravelog.models.comment import Comment
from mytravelog.models.follower import Follower
from mytravelog.models.like import Like
from mytravelog.models.log import Log
from mytravelog.models.log_picture import LogPicture
from mytravelog.models.user_profile import UserProfile
from mytravelog.views.user import attach_additional_info_to_logs, is_requested_user_followed_by_current_user

__author__ = 'Manas'


def create_log(request):
    if request.is_ajax():
        user = request.user
        return_data = {}
        if user.is_authenticated():
            post_data = request.POST
            file_data = request.FILES
            location = post_data.get('location', '')
            if ',' in location:
                location = location[0:location.index(',')]
            latitude = post_data.get('latitude', '')
            longitude = post_data.get('longitude', '')
            album_name = post_data.get('album_name', '')
            description = post_data.get('description', '')

            # validate log data
            validation_output = validate_log_form(location, latitude, longitude, description, len(file_data))
            error = validation_output.get('error', None)
            if error is None:
                # get user_profile, album and city associated with this log
                user_profile = UserProfile.objects.get(user=user)
                city = validation_output['city']
                if album_name != "None":
                    album = Album.objects.get(name=album_name, user_profile=user_profile)
                else:
                    album = None

                # create a new log
                new_log = Log()
                new_log.user_profile = user_profile
                new_log.city = city
                new_log.latitude = latitude
                new_log.longitude = longitude
                new_log.album = album
                new_log.description = description
                new_log.score = 0
                new_log.save()

                # now that we have created_at, update the log score and re-save
                new_log.score = get_log_score(new_log)
                new_log.save()

                # create new log picture for every image submitted by user
                for key, image_file in file_data.iteritems():
                    new_log_picture = LogPicture()
                    new_log_picture.log = new_log
                    new_log_picture.picture = image_file
                    new_log_picture.save()

            else:
                return_data['error'] = error

            return_data = json.dumps(return_data)
            mimetype = "application/json"
            return HttpResponse(return_data, mimetype)
        else:
            return_data['redirect_to'] = '/mytravelog/sign_in/'
    else:
        raise Http404


def delete_log(request, log_id):
    user = request.user
    return_data = {}
    if request.is_ajax():
        if user.is_authenticated():
            log_to_delete = Log.objects.get(id=log_id)
            # check if log belongs to current user
            if log_to_delete.user_profile.user == user:
                # delete log
                log_to_delete.delete()
            else:
                return_data['error'] = "This log does not belong to you"
        else:
            return_data['redirect_to'] = "/mytravelog/sign_in/"

        return_data = json.dumps(return_data)
        mimetype = "application/json"
        return HttpResponse(return_data, mimetype)
    else:
        raise Http404


def edit_log(request, log_id):
    if request.is_ajax():
        user = request.user
        return_data = {}
        if user.is_authenticated():
            post_data = request.POST
            file_data = request.FILES
            album_name = post_data.get('album_name', '')
            description = post_data.get('description', '')
            # get list of picture ids to remove and remove empty string at the end
            delete_picture_ids = post_data.get('images_to_delete', '').split(',')
            delete_picture_ids.pop()

            # get log that has to be edited along with all the pictures associated with it
            log_to_edit = Log.objects.get(id=log_id)
            if log_to_edit.user_profile.user == user:
                log_pictures = LogPicture.objects.filter(log=log_to_edit)

                # validate log data
                error = validate_edit_log_form(description, len(delete_picture_ids), len(file_data), len(log_pictures))
                if error is None:
                    # update existing log
                    user_profile = UserProfile.objects.get(user=user)
                    if album_name != "None":
                        log_to_edit.album = Album.objects.get(name=album_name, user_profile=user_profile)
                    else:
                        log_to_edit.album = None
                    log_to_edit.description = description
                    log_to_edit.save()

                    # remove log pictures requested by user
                    for picture_id in delete_picture_ids:
                        LogPicture.objects.get(id=picture_id).delete()

                    # create new log picture for every image submitted by user
                    for key, image_file in file_data.iteritems():
                        new_log_picture = LogPicture()
                        new_log_picture.log = log_to_edit
                        new_log_picture.picture = image_file
                        new_log_picture.save()

                else:
                    return_data['error'] = error
            else:
                return_data['error'] = "This log does not belong to you"

            return_data = json.dumps(return_data)
            mimetype = "application/json"
            return HttpResponse(return_data, mimetype)
        else:
            return_data['redirect_to'] = '/mytravelog/sign_in/'
    else:
        raise Http404


def show_log(request, log_id):
    # get requested user log and put it in a list, since logs template and helper functions only accept a list of logs
    requested_log = [get_object_or_404(Log, id=log_id)]

    # get current user and user profile
    current_user = request.user
    current_user_profile = None
    if current_user.is_authenticated():
        current_user_profile = UserProfile.objects.get(user=current_user)

    # get requested user and user profile
    requested_user_profile = requested_log[0].user_profile
    requested_user = requested_user_profile.user

    # attach additional info to the requested log (likes, comments and pictures)
    attach_additional_info_to_logs(requested_log, current_user_profile)

    # get all requested albums in order to populate the Albums drop-down list while editing a log (EditLogModal)
    requested_user_albums = Album.objects.filter(user_profile=requested_user_profile)

    # check if requested user can be followed by current user
    # if yes, then check if requested user is being followed by current user
    can_follow = False
    is_followed = False
    if current_user != requested_user and current_user_profile is not None:
        can_follow = True
        is_followed = is_requested_user_followed_by_current_user(requested_user_profile, current_user_profile)

    # check if current user can edit profile
    can_edit_profile = False
    if current_user == requested_user:
        can_edit_profile = True

    data_dict = {
        'requested_user': requested_user,
        'requested_user_profile': requested_user_profile,
        'current_user_profile': current_user_profile,
        'requested_user_albums': requested_user_albums,
        'requested_log': requested_log,
        'can_follow': can_follow,
        'is_followed': is_followed,
        'can_edit_profile': can_edit_profile
    }
    return render(request, 'mytravelog/user_log.html', data_dict)


def get_log_positions(request, username):
    return_data = {}
    if request.is_ajax():
        all_user_logs = Log.objects.filter(user_profile__user=get_object_or_404(User, username=username))
        log_positions = {}
        for log in all_user_logs:
            log_positions[log.id] = {'city': log.city.name,
                                     'date_and_time': str(log.created_at),
                                     'latitude': str(log.latitude),
                                     'longitude': str(log.longitude)}
        return_data['all_positions'] = log_positions

        return_data = json.dumps(return_data)
        mimetype = "application/json"
        return HttpResponse(return_data, mimetype)
    else:
        raise Http404


def show_live_feed(request, feed_filter):
    # get current user and user profile
    current_user = request.user
    current_user_profile = None
    if current_user.is_authenticated():
        current_user_profile = UserProfile.objects.get(user=current_user)

    # filter logs based on feed filter and sort them by decreasing order of score
    if feed_filter == 'all':
        # get all logs
        requested_logs = Log.objects.order_by('-score')
    elif feed_filter == 'following':
        # check if user is authenticated
        if current_user_profile is not None:
            # only get logs of users followed by current user
            current_user_following = Follower.objects.filter(follower_user_profile=current_user_profile).values('following_user_profile')
            requested_logs = Log.objects.filter(user_profile__in=current_user_following).order_by('-score')
        else:
            return HttpResponseRedirect('/mytravelog/sign_in')
    else:
        raise Http404

    # paginate the logs
    paginator = Paginator(requested_logs, 10)
    page_num = request.GET.get('page')
    try:
        requested_page_logs = paginator.page(page_num)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        requested_page_logs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        requested_page_logs = paginator.page(paginator.num_pages)

    # attach additional info (likes, comments and pictures) to page logs
    requested_page_logs = attach_additional_info_to_logs(requested_page_logs, current_user_profile)

    # get all albums for the current user in order to populate the Albums drop-down list while
    # editing a log (EditLogModal)
    current_user_albums = Album.objects.filter(user_profile=current_user_profile)

    data_dict = {
        'current_user_profile': current_user_profile,
        'current_user_albums': current_user_albums,
        'requested_page_logs': requested_page_logs,
        'requested_filter': feed_filter
    }
    return render(request, 'mytravelog/live_feed.html', data_dict)


# ---------------Helper functions----------------

def validate_log_form(location, latitude, longitude, description, number_of_pictures):
    output = {}
    if len(location) == 0 or len(latitude) == 0 or len(longitude) == 0:
        output['error'] = "Your location could not be verified"
    elif len(description) == 0:
        output['error'] = "Description is required"
    elif len(description) > 1000:
        output['error'] = "Description length cannot exceed 1000 characters"
    elif number_of_pictures == 0:
        output['error'] = "At least one image is required"
    else:
        city = City.objects.filter(name=location)
        if len(city) == 1:
            output['city'] = city[0]
        else:
            output['error'] = "No city named '" + location + "' in the database"
    return output


def validate_edit_log_form(description, number_of_pictures_to_delete, number_of_pictures_to_add, total_number_of_pictures):
    if len(description) == 0:
        return "Description is required"
    elif len(description) > 1000:
        return "Description length cannot exceed 1000 characters"
    elif (total_number_of_pictures - number_of_pictures_to_delete + number_of_pictures_to_add) == 0:
        return "At least one image is required"
    else:
        return None


# score function: log_score = log10(z) + (time_since_epoch/45000)
# where z = num_likes + num_comments (z=1 if (num_likes + num_comments) == 0)
def get_log_score(log_to_score):
    # only consider likes and comments made my other users, and not the user who created the log
    num_comments = Comment.objects.filter(Q(log=log_to_score) & ~Q(commenter_user_profile=log_to_score.user_profile)).count()
    num_likes = Like.objects.filter(Q(log=log_to_score) & ~Q(liker_user_profile=log_to_score.user_profile)).count()
    log_created_at = log_to_score.created_at.replace(tzinfo=None)  # remove time zone awareness
    time_since_epoch = (log_created_at - datetime.datetime(1970, 1, 1)).total_seconds() / 45000
    z = (num_likes + num_comments)
    if z == 0:
        z = 1
    score = round(math.log(z, 10) + time_since_epoch, 7)
    return score