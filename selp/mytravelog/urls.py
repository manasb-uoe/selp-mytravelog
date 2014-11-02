from django.conf.urls import patterns, url
from mytravelog.views import search, album
from views import home, user, city

__author__ = 'Manas'

urlpatterns = patterns('',
                       url(r'^$', home.home),
                       url(r'^sign_up/$', user.sign_up),
                       url(r'^sign_in/$', user.sign_in),
                       url(r'^sign_out/$', user.sign_out),
                       url(r'^city/autocomplete/$', city.get_autocomplete_suggestions),
                       url(r'^city/(?P<city_url_name>\w+)/$', city.show_city),
                       url(r'^search/$', search.search_for_cities_and_users),
                       url(r'^user/(?P<username>\w+)/albums/$', user.show_user_albums)
                       )
