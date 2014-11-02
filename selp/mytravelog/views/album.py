import json
import re
import datetime
from django.http.response import Http404, HttpResponse, HttpResponseRedirect
from mytravelog.models.album import Album
from mytravelog.models.user_profile import UserProfile

__author__ = 'Manas'


def create_album(request):
    if request.is_ajax():
        user = request.user
        return_data = {}
        if user.is_authenticated():
            post_data = request.POST
            name = post_data.get('name', "")
            url_name = re.sub(r'\s', '_', name)
            start_date = post_data.get('start_date', "")
            end_date = post_data.get('end_date', "")
            cover_picture = request.FILES.get('cover_picture', None)
            print "-----------------------------1"

            # validate album data
            user_profile = UserProfile.objects.get(user=user)
            error = validate_album_form(user_profile, name, start_date, end_date)
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

                    # send redirection url if album is created successfully
                    return_data['redirect_to'] = "/mytravelog/user/" + user.username + "/albums/"
        else:
            return_data['redirect_to'] = "/mytravelog/sign_in/"

        return_data = json.dumps(return_data)
        mimetype = "application/json"
        return HttpResponse(return_data, mimetype)
    else:
        raise Http404


# -------------------HELPER FUNCTIONS--------------------

def validate_album_form(user_profile, name, start_date, end_date):
    print "-----------------------------2"
    if len(name) == 0:
        return "Album name is required"
    if name.lower() == "none":
        return "Album name cannot be 'None'"
    # check if an album with the same name already exists for current user
    albums_with_same_name = Album.objects.filter(name=name, user_profile=user_profile)
    if len(albums_with_same_name) > 0:
        return "You already have an album with the same name"
    if len(start_date) == 0:
        return "Start date is required"
    if len(end_date) == 0:
        return "End date is required"
    return None


def convert_string_to_date(string_date):
    split = string_date.split("-")
    date = datetime.date(int(split[0]), int(split[1]), int(split[2]))  # format: year-month-date
    return date