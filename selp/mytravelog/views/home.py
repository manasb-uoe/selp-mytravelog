from django.http.response import HttpResponse
from django.shortcuts import render

__author__ = 'Manas'


def home(request):
    return render(request, 'mytravelog/home.html')