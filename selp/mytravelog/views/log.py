import json
from django.http.response import Http404, HttpResponse
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
            album_name = post_data.get('album_name', '')
            description = post_data.get('description', '')

            # validate log data
            validation_output = validate_log_form(location, description)
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


def validate_log_form(location, description):
    output = {}
    if len(location) == 0:
        output['error'] = "Location/Current city is required"
    elif len(description) == 0:
        output['error'] = "Description is required"
    else:
        city = City.objects.filter(name=location)
        if len(city) == 1:
            output['city'] = city[0]
        else:
            output['error'] = "No city named '" + location + "' in the database"
    return output