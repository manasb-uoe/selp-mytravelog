import json

from django.db.models.query_utils import Q
from django.http.response import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render

from mytravelog.models.album import Album
from mytravelog.models.city import City
from mytravelog.models.log import Log
from mytravelog.models.user_profile import UserProfile


__author__ = 'Manas'


def show_city(request, city_url_name):
    # get city using the url name provided
    # else, show 404 error
    requested_city = get_object_or_404(City, url_name=city_url_name)

    # get current user and user profile
    current_user = request.user
    current_user_profile = None
    if current_user.is_authenticated():
        current_user_profile = UserProfile.objects.get(user=current_user)

    # get all albums for the current user in order to populate the Albums drop-down list while
    # editing a log (EditLogModal)
    current_user_albums = Album.objects.get_user_albums_with_duration(current_user_profile)

    # get all city logs
    requested_city_logs = Log.objects.attach_additional_info_to_logs(Log.objects.get_city_logs(requested_city),
                                                                     current_user_profile)

    data_dict = {
        'requested_city': requested_city,
        'current_user_profile': current_user_profile,
        'requested_city_logs': requested_city_logs,
        'current_user_albums': current_user_albums
    }
    return render(request, 'mytravelog/city.html', data_dict)


def get_autocomplete_suggestions(request):
    if request.is_ajax():
        search_term = request.GET.get('search_term', None)
        if search_term is not None:
            cities = City.objects.filter(Q(name__startswith=search_term) | Q(country_name__startswith=search_term))
            return_data = []
            for city in cities:
                city_json = {'city': city.name, 'country': city.country_name}
                return_data.append(city_json)
            return_data = json.dumps(return_data)
            mimetype = "application/json"
            return HttpResponse(return_data, mimetype)
    raise Http404
