from django.conf.urls import patterns, url
from mytravelog.views import search, album, log, like, comment
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
                       url(r'^user/(?P<username>\w+)/$', user.show_user),
                       url(r'^album/create/$', album.create_album),
                       url(r'^album/update/(?P<album_id>\w+)/$', album.update_album),
                       url(r'^album/delete/(?P<album_id>\w+)/$', album.delete_album),
                       url(r'^log/create/$', log.create_log),
                       url(r'^log/delete/(?P<log_id>\w+)/$', log.delete_log),
                       url(r'^log/edit/(?P<log_id>\w+)/$', log.edit_log),
                       url(r'^like/(?P<log_id>\w+)/$', like.like_log),
                       url(r'^dislike/(?P<log_id>\w+)/$', like.dislike_log),
                       url(r'^comment/create/(?P<log_id>\w+)/$', comment.create_log_comment),
                       url(r'^comment/delete/(?P<comment_id>\w+)/$', comment.delete_log_comment)
)
