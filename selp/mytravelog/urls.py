from django.conf.urls import patterns, url
from views import home, user, city

__author__ = 'Manas'

urlpatterns = patterns('',
                        url(r'^$', home.home),
                        url(r'^sign_up/$', user.sign_up),
                        url(r'^sign_in/$', user.sign_in),
                        url(r'^sign_out/$', user.sign_out),
                        url(r'^city/(?P<city_url_name>\w+)/$', city.show_city)
)