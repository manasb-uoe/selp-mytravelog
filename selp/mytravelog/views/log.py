import json
from django.contrib.auth.models import User
from django.http.response import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from mytravelog.models.album import Album
from mytravelog.models.city import City
from mytravelog.models.log import Log
from mytravelog.models.log_picture import LogPicture
from mytravelog.models.user_profile import UserProfile

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


# ---------------Helper functions----------------

def validate_log_form(location, latitude, longitude, description, number_of_pictures):
    output = {}
    if len(location) == 0 or len(latitude) == 0 or len(longitude) == 0:
        output['error'] = "Your location could not be verified"
    elif len(description) == 0:
        output['error'] = "Description is required"
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
    elif (total_number_of_pictures - number_of_pictures_to_delete + number_of_pictures_to_add) == 0:
        return "At least one image is required"
    else:
        return None