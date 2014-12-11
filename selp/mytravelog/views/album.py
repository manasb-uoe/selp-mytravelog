import json
import re
import datetime

from django.http.response import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render

from mytravelog.models.album import Album
from mytravelog.models.follower import Follower
from mytravelog.models.log import Log
from mytravelog.models.user_profile import UserProfile


__author__ = 'Manas'


def create_album(request):
    """
    Uses create_or_update_album helper function in order to
    create a new album. It passes 'create' operation to this
    function along with the request and id of the album. Although,
    since an album is being created, an id of -1 is passed instead.
    Also note that this view only accepts ajax requests, else a 404
    error is raised.
    """
    if request.is_ajax():
        return_data = create_or_update_album(request, 'create', -1)
        return_data = json.dumps(return_data)
        mimetype = "application/json"
        return HttpResponse(return_data, mimetype)
    else:
        raise Http404


def update_album(request, album_id):
    """
    Uses create_or_update_album helper function in order to
    update an existing album. It passes 'update' operation to this
    function along with the request and id of the album being updated.
    Also note that this view only accepts ajax requests, else a 404
    error is raised.
    """
    if request.is_ajax():
        return_data = create_or_update_album(request, 'update', album_id)
        return_data = json.dumps(return_data)
        mimetype = "application/json"
        return HttpResponse(return_data, mimetype)
    else:
        raise Http404


def delete_album(request, album_id):
    """
    Deletes an album with the provided album_id. It first
    checks if the album actually belongs to the user
    who sent the request. If this is not the case, then
    an error is sent back. Else, the album is successfully
    deleted. Also note that this view only accepts ajax
    requests, else a 404 error is raised.
    """
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
    """
    Renders user_album template using the the data of the
    album with the provided album_id.
    """
    # get requested user album and attach duration to it
    requested_album = get_object_or_404(Album, id=album_id)
    duration = (requested_album.end_date - requested_album.start_date).days
    requested_album.duration = duration

    # get current user and user profile
    current_user = request.user
    current_user_profile = None
    if current_user.is_authenticated():
        current_user_profile = UserProfile.objects.get(user=current_user)

    # get requested user and user profile
    requested_user_profile = requested_album.user_profile
    requested_user = requested_user_profile.user

    # get all album logs and pictures
    requested_album_logs = Log.objects.attach_additional_info_to_logs(Log.objects.get_album_logs(requested_album),
                                                          current_user_profile)
    album_pictures = []
    for log in requested_album_logs:
        album_pictures += log.pictures
    requested_album.pictures = album_pictures

    # get all requested albums in order to populate the Albums drop-down list while editing a log (EditLogModal)
    requested_user_albums = Album.objects.get_user_albums_with_duration(requested_user_profile)

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
        'requested_album': requested_album,
        'requested_album_logs': requested_album_logs,
        'can_follow': can_follow,
        'is_followed': is_followed,
        'can_edit_profile': can_edit_profile
    }
    return render(request, 'mytravelog/user_album.html', data_dict)


# -------------------HELPER FUNCTIONS--------------------
def create_or_update_album(request, operation, album_id):
    """
    Creates or updates an album based on the provided operation.
    :param request: HttpRequest instance received by the view
    :param operation: Takes two values: 'create' or 'update'
    :param album_id: Id of the album that needs to be updated. Id will be ignored if operation = 'create'
    :return: Dict containing an error message or a redirection url. If no errors occur, then this dict is empty
    """
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
            error = validate_album_form(operation, user_profile, name, start_date, end_date, None, cover_picture)
        else:
            album_to_update = Album.objects.get(id=album_id)
            error = validate_album_form(operation, user_profile, name, start_date, end_date, album_to_update, cover_picture)
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


def validate_album_form(operation, user_profile, name, start_date, end_date, album_to_update, cover_picture):
    """
    Validates all the album data provided. Returns an error message if any error occurs, else None is returned
    :param operation: Takes two values: 'create' or 'update'
    :param user_profile: UserProfile instance for the current user
    :param name: Name of the album
    :param start_date: Start data of the album as a String
    :param end_date: End date of the album as a String
    :param album_to_update: Album instance to update. Only needed when operation = 'update'
    :param cover_picture: cover picture file instance from request.FILES
    :return: error message as a String if an error occurs, else None
    """
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
    if cover_picture is not None:
        if cover_picture._size > 2048*1024:
            return "Max image size allowed is 2 mb"
    return None


def convert_string_to_date(string_date):
    """
    Converts a string date into datetime date instance
    :param string_date: Date as a string
    :return: datetime date instance
    """
    split = string_date.split("-")
    date = datetime.date(int(split[0]), int(split[1]), int(split[2]))  # format: year-month-date
    return date
