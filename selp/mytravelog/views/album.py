import json
import re
import datetime

from django.http.response import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render

from mytravelog.models.album import Album
from mytravelog.models.log import Log
from mytravelog.models.user_profile import UserProfile
from mytravelog.views.user import attach_additional_info_to_logs, get_all_user_permissions, \
    is_requested_user_followed_by_current_user


__author__ = 'Manas'


def create_album(request):
    if request.is_ajax():
        return_data = create_or_update_album(request, 'create', -1)
        return_data = json.dumps(return_data)
        mimetype = "application/json"
        return HttpResponse(return_data, mimetype)
    else:
        raise Http404


def update_album(request, album_id):
    if request.is_ajax():
        return_data = create_or_update_album(request, 'update', album_id)
        return_data = json.dumps(return_data)
        mimetype = "application/json"
        return HttpResponse(return_data, mimetype)
    else:
        raise Http404


def delete_album(request, album_id):
    user = request.user
    return_data = {}
    if request.is_ajax():
        if user.is_authenticated():
            album_to_delete = Album.objects.get(id=album_id)
            # check if album belongs to current user
            if album_to_delete.user_profile.user.username == user.username:
                # delete album
                album_to_delete.delete()
            else:
                return_data['error'] = "This album does not belong to you"
        else:
            return_data['redirect_to'] = "/mytravelog/sign_in/"

        return_data = json.dumps(return_data)
        mimetype = "application/json"
        return HttpResponse(return_data, mimetype)
    else:
        raise Http404


def show_album(request, album_id):
    # get requested user album and attach duration to it
    requested_album = get_object_or_404(Album, id=album_id)
    duration = (requested_album.end_date - requested_album.start_date).days
    requested_album.duration = duration
    data_dict = get_all_user_permissions(requested_album.user_profile.user, request.user)

    # get all album logs and pictures
    requested_album_logs = attach_additional_info_to_logs(Log.objects.filter(album=requested_album),
                                                          data_dict.get('current_user_profile', None))
    data_dict['requested_album_logs'] = requested_album_logs
    album_pictures = []
    for log in requested_album_logs:
        album_pictures += log.pictures
    requested_album.pictures = album_pictures
    data_dict['requested_album'] = requested_album

    # get all requested albums in order to populate the Albums dropdown list while editing a log (EditLogModal)
    requested_user_albums = Album.objects.filter(user_profile=data_dict['requested_user_profile'])
    data_dict['requested_user_albums'] = requested_user_albums

    # check if requested user is being followed by current user
    is_requested_user_followed_by_current_user(data_dict)

    return render(request, 'mytravelog/user_album.html', data_dict)


# -------------------HELPER FUNCTIONS--------------------
def create_or_update_album(request, operation, album_id):
    user = request.user
    return_data = {}
    if user.is_authenticated():
        post_data = request.POST
        name = post_data.get('name', "")
        url_name = re.sub(r'\s', '_', name)
        start_date = post_data.get('start_date', "")
        end_date = post_data.get('end_date', "")
        cover_picture = request.FILES.get('cover_picture', None)

        # validate album data
        album_to_update = None
        user_profile = UserProfile.objects.get(user=user)
        if operation == 'create':
            error = validate_album_form(operation, user_profile, name, start_date, end_date, None)
        else:
            album_to_update = Album.objects.get(id=album_id)
            error = validate_album_form(operation, user_profile, name, start_date, end_date, album_to_update)
        if error is not None:
            return_data['error'] = error
        else:
            # convert string dates to datetime.date
            start_date = convert_string_to_date(start_date)
            end_date = convert_string_to_date(end_date)

            # one final check to confirm if end_date comes after start_date
            if (end_date - start_date).days < 0:
                return_data['error'] = "End date must come after Start date"
            else:
                if operation == 'create':
                    # create new album
                    new_album = Album()
                    new_album.user_profile = user_profile
                    new_album.name = name
                    new_album.url_name = url_name
                    new_album.start_date = start_date
                    new_album.end_date = end_date
                    if cover_picture is not None:
                        new_album.cover_picture = cover_picture
                    new_album.save()
                else:
                    # update existing album
                    album_to_update.name = name
                    album_to_update.url_name = url_name
                    album_to_update.start_date = start_date
                    album_to_update.end_date = end_date
                    if cover_picture is not None:
                        album_to_update.cover_picture = cover_picture
                    album_to_update.save()

    else:
        return_data['redirect_to'] = "/mytravelog/sign_in/"

    return return_data


def validate_album_form(operation, user_profile, name, start_date, end_date, album_to_update):
    if len(name) == 0:
        return "Album name is required"
    if name.lower() == "none":
        return "Album name cannot be 'None'"
    if operation == "create":
        # check if an album with the same name already exists for current user
        albums_with_same_name = Album.objects.filter(name=name, user_profile=user_profile)
        if len(albums_with_same_name) > 0:
            return "You already have an album with the same name"
    else:
        if name != album_to_update.name:
            # check if an album with the same name already exists for current user
            albums_with_same_name = Album.objects.filter(name=name, user_profile=user_profile)
            if len(albums_with_same_name) > 0:
                return "You already have an album with the same name"
        # check if album belongs to current user
        if album_to_update.user_profile.user.username != user_profile.user.username:
            return "This album does not belong to you"
    if len(start_date) == 0:
        return "Start date is required"
    if len(end_date) == 0:
        return "End date is required"
    return None


def convert_string_to_date(string_date):
    split = string_date.split("-")
    date = datetime.date(int(split[0]), int(split[1]), int(split[2]))  # format: year-month-date
    return date
