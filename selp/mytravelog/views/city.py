import json
from django.db.models.query_utils import Q
from django.http.response import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from mytravelog.models.city import City

__author__ = 'Manas'


def show_city(request, city_url_name):
    # get city using the url name provided
    # else, show 404 error
    requested_city = get_object_or_404(City, url_name=city_url_name)

    # convert city tourist count to millions
    tourist_count = requested_city.tourist_count
    requested_city.tourist_count = tourist_count/1000000.0

    data_dict = {'requested_city': requested_city}
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