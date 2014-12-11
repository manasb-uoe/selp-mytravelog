import json

from django.contrib.auth.models import User
from django.http.response import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render

from mytravelog.models.album import Album
from mytravelog.models.city import City
from mytravelog.models.follower import Follower
from mytravelog.models.log import Log
from mytravelog.models.log_picture import LogPicture
from mytravelog.models.user_profile import UserProfile


__author__ = 'Manas'


def create_log(request):
    """
    Creates a new log using the provided POST data. First, the
    provided POST data is validated, if no errors are returned,
    then a log is created successfully. Also, new LogPicture is
    created for each of the pictures in the POST data. Also note
    that this view only accepts ajax requests, else a 404 error
    is raised.
    """
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
            error = validate_add_log_form(location, latitude, longitude, description, file_data)
            if error is None:
                # get user_profile, album and city associated with this log
                user_profile = UserProfile.objects.get(user=user)
                city = City.objects.get(name=location)
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
                new_log.score = new_log.get_log_score()
                new_log.save()

                # create new log picture for every image submitted by user
                for key, image_file in file_data.iteritems():
                    new_log_picture = LogPicture()
                    new_log_picture.log = new_log
                    new_log_picture.picture = image_file
                    new_log_picture.save()

                # finally, update user travel stats
                user_profile.update_user_travel_stats()

            else:
                return_data['error'] = error
        else:
            return_data['redirect_to'] = '/mytravelog/sign_in/'

        return_data = json.dumps(return_data)
        mimetype = "application/json"
        return HttpResponse(return_data, mimetype)

    else:
        raise Http404


def delete_log(request, log_id):
    """
    Deletes the log with the provided log_id. It first
    checks if the log actually belongs to the current user.
    If this is not the case, then an error message is returned.
    Else, the log is successfully deleted. Also note that this
    view only accepts ajax requests, else a 404 error is raised.
    """
    user = request.user
    return_data = {}
    if request.is_ajax():
        if user.is_authenticated():
            log_to_delete = Log.objects.get_log_by_id(log_id)
            # check if log belongs to current user
            if log_to_delete.user_profile.user == user:
                # delete log and update user travel stats
                log_to_delete.delete()
                UserProfile.objects.get(user=user).update_user_travel_stats()
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
    """
    Updates the log with the provided id, using the POST data provided.
    It also checks if the log actually belongs to the current user. If
    this is not the case, then an error message is returned. Else, the
    log is updated successfully. Also, the LogPicture instances are deleted
    based on the on the delete_picture_ids list in POST data. Also note that
    this view only accepts ajax requests, else a 404 error is raised.
    """
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
            log_to_edit = Log.objects.get_log_by_id(log_id)
            if log_to_edit.user_profile.user == user:
                log_pictures = LogPicture.objects.filter(log=log_to_edit)

                # validate log data
                error = validate_edit_log_form(description, len(delete_picture_ids), file_data, len(log_pictures))
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
        else:
            return_data['redirect_to'] = '/mytravelog/sign_in/'

        return_data = json.dumps(return_data)
        mimetype = "application/json"
        return HttpResponse(return_data, mimetype)

    else:
        raise Http404


def show_log(request, log_id):
    """
    Renders the user_log template using the data of the log with the
    provided log_id.
    """
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
    Log.objects.attach_additional_info_to_logs(requested_log, current_user_profile)

    # get all requested albums in order to populate the Albums drop-down list while editing a log (EditLogModal)
    requested_user_albums = Album.objects.filter(user_profile=requested_user_profile)

    # check if requested user can be followed by current user
    # if yes, then check if requested user is being followed by current user
    can_follow = False
    is_followed = False
    if current_user != requested_user and current_user_profile is not None:
        can_follow = True
        is_followed = Follower.objects.is_requested_user_followed_by_current_user(requested_user_profile, current_user_profile)

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


def get_log_info_for_map(request, username):
    """
    Returns a dict where each log id is mapped to their info. The log info
    that is returned in filtered using the username provided. Also note that
    this view only accepts ajax requests, else a 404 error is raised.
    """
    return_data = {}
    if request.is_ajax():
        all_user_logs = Log.objects.filter(user_profile__user=get_object_or_404(User, username=username))
        user_logs_info = {}
        for log in all_user_logs:
            user_logs_info[log.id] = {
                'city': log.city.name,
                'date_and_time': str(log.created_at),
                'latitude': str(log.latitude),
                'longitude': str(log.longitude),
                'url': '/mytravelog/log/' + str(log.id) + '/'
            }
        return_data['user_logs_info'] = user_logs_info

        return_data = json.dumps(return_data)
        mimetype = "application/json"
        return HttpResponse(return_data, mimetype)
    else:
        raise Http404


# ---------------Helper functions----------------

def validate_add_log_form(location, latitude, longitude, description, file_data):
    """
    Validates the provided log data and returns an error message, if any error occurs, else, None is returned.
    :param location: name of the city where the log is created
    :param latitude: latitude of the location
    :param longitude: longitude of the location
    :param description: description of the log
    :param file_data: dict of all files in POST data, i.e. request.FILES
    :return: an error message if any error occurs, else, None is returned.
    """
    if len(location) == 0 or len(latitude) == 0 or len(longitude) == 0:
        return "Your location could not be verified"
    if len(description) == 0:
        return "Description is required"
    if len(description) > 1000:
        return "Description length cannot exceed 1000 characters"
    if len(file_data) == 0:
        return "At least one image is required"
    if len(file_data) > 10:
        return "At most 10 images are allowed"
    for key, image_file in file_data.iteritems():
        if (image_file._size > 2048*1024):
            return "Max image size allowed is 2 mb"
    if City.objects.filter(name=location).count() == 0:
        return "No city named '" + location + "' in the database"
    return None


def validate_edit_log_form(description, number_of_pictures_to_delete, file_data, total_number_of_pictures):
    """
    Validates the log data provided.
    :param description: description of the log
    :param number_of_pictures_to_delete: total number of picture to be deleted
    :param file_data: dict of all files in POST data, i.e. request.FILES
    :param total_number_of_pictures: total number of existing log pictures
    :return: an error message if any error occurs, else, None is returned
    """
    if len(description) == 0:
        return "Description is required"
    if len(description) > 1000:
        return "Description length cannot exceed 1000 characters"
    number_of_pictures_to_add = len(file_data)
    remaining_pictures = total_number_of_pictures - number_of_pictures_to_delete + number_of_pictures_to_add
    if remaining_pictures == 0:
        return "At least one image is required"
    if remaining_pictures > 10:
        return "At most 10 images are allowed"
    for key, image_file in file_data.iteritems():
        if (image_file._size > 2048*1024):
            return "Max image size allowed is 2 mb"
    return None




