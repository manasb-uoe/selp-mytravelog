from django.http.response import HttpResponse
from django.shortcuts import render
from mytravelog.models.city import City

__author__ = 'Manas'


def home(request):
    # get top 12 cities based on tourist count
    popular_cities = City.objects.order_by('-tourist_count')[:12]
    data_dict = {'popular_cities': popular_cities}
    return render(request, 'mytravelog/home.html', data_dict)