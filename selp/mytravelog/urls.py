from django.conf.urls import patterns, url
from views import home

__author__ = 'Manas'

urlpatterns = patterns('',
                        url(r'^$', home.home)
)