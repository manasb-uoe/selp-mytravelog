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