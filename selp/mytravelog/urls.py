from django.conf.urls import patterns, url
from views import home, user

__author__ = 'Manas'

urlpatterns = patterns('',
                        url(r'^$', home.home),
                        url(r'sign_up/$', user.sign_up)
)