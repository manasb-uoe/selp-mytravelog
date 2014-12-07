import os
from django.contrib.auth.models import User
from django.core.files.base import File
from mytravelog.models.album import Album
from mytravelog.models.city import City
from mytravelog.models.like import Like
from mytravelog.models.log import Log
from mytravelog.models.log_picture import LogPicture
from mytravelog.models.user_profile import UserProfile
from mytravelog.views.city import add_new_city

__author__ = 'Manas'

urls = {
    'home': '/mytravelog/',
    'sign_up': '/mytravelog/sign_up/',
    'sign_in': '/mytravelog/sign_in/',
    'sign_out': '/mytravelog/sign_out/',
    'user_base': '/mytravelog/user/',
    'city_base': '/mytravelog/city/',
    'city_autocomplete': '/mytravelog/city/autocomplete/',
    'search_base': '/mytravelog/search/',
    'album_create': '/mytravelog/album/create/',
    'album_update_base': '/mytravelog/album/update/',
    'album_delete_base': '/mytravelog/album/delete/',
    'album_show_base': '/mytravelog/album/',
    'log_create': '/mytravelog/log/create/',
    'log_update_base': '/mytravelog/log/edit/',
    'log_delete_base': '/mytravelog/log/delete/',
    'log_show_base': '/mytravelog/log/',
    'log_get_info_for_map_base': '/mytravelog/log/get_info_for_map/',
    'log_show_live_feed_base': '/mytravelog/live_feed/',
    'like_create_base': '/mytravelog/like/create/',
    'like_delete_base': '/mytravelog/like/delete/'
}

city1_sample_data = {
    'name': 'city1',
    'country_name': 'country1',
    'tourist_count': 1,
    'tourist_growth': 2,
    'description': 'desc1'
}
city2_sample_data = {
    'name': 'city2',
    'country_name': 'country2',
    'tourist_count': 2,
    'tourist_growth': 2,
    'description': 'desc2'
}

user1_sample_data = {
    'username': 'username1',
    'password': 'password',
    'first_name': 'user',
    'last_name': '1',
    'email': 'email@email.com'
}

album1_sample_data = {
    'name': 'album1',
    'start_date': '2014-8-24',
    'end_date': '2014-9-28'
}

album2_sample_data = {
    'name': 'album2',
    'start_date': '2014-8-29',
    'end_date': '2014-10-22'
}

log1_sample_data = {
    'latitude': 0.0,
    'longitude': 0.0,
    'description': 'desc1'
}

log2_sample_data = {
    'latitude': 26.0,
    'longitude': 54.0,
    'description': 'desc2'
}

large_image_path = os.path.join(os.path.join(os.path.dirname(__file__), 'test_images'), 'large_image.jpg')

small_image_path = os.path.join(os.path.join(os.path.dirname(__file__), 'test_images'), 'small_image.jpg')


def add_sample_city(city_sample_data):
    add_new_city(name=city_sample_data['name'],
                 country_name=city_sample_data['country_name'],
                 tourist_count=city_sample_data['tourist_count'],
                 tourist_growth=city_sample_data['tourist_growth'],
                 description=city_sample_data['description'])


def add_sample_user_and_user_profile(user_sample_data):
    user = User()
    user.username = user_sample_data['username']
    user.set_password(user_sample_data['password'])
    user.first_name = user_sample_data['first_name']
    user.last_name = user_sample_data['last_name']
    user.email = user_sample_data['email']
    user.save()
    user_profile = UserProfile()
    user_profile.user = user
    user_profile.save()
    return user


def get_large_image():
    return open(large_image_path, 'rb')


def get_small_image():
    return open(small_image_path, 'rb')


def get_user_and_user_profile(user_sample_data):
    sample_user = User.objects.get(username=user_sample_data['username'])
    sample_user_profile = UserProfile.objects.get(user=sample_user)
    return {
        'user': sample_user,
        'user_profile': sample_user_profile
    }


def add_sample_album(album_sample_data, user_sample_data):
    album = Album()
    album.name = album_sample_data['name']
    album.start_date = album_sample_data['start_date']
    album.end_date = album_sample_data['end_date']
    user_profile = UserProfile.objects.get(user__username=user_sample_data['username'])
    album.user_profile = user_profile
    album.save()


def get_album(album_sample_data, user_sample_data):
    album = Album.objects.get(name=album_sample_data['name'],
                              user_profile__user__username=user_sample_data['username'])
    album.duration = (album.end_date - album.start_date).days
    return album


def add_sample_log(log_sample_data, album_sample_data, city_sample_data, user_sample_data):
    log = Log()
    log.city = City.objects.get(name=city_sample_data['name'])
    log.latitude = log_sample_data['latitude']
    log.longitude = log_sample_data['longitude']
    log.description = log_sample_data['description']
    user_profile = UserProfile.objects.get(user__username=user_sample_data['username'])
    log.user_profile = user_profile
    log.album = Album.objects.get(name=album_sample_data['name'], user_profile=user_profile)
    log.score = 0
    log.save()
    log_picture = LogPicture()
    log_picture.log = log
    log_picture.picture = File(get_small_image())
    log_picture.save()

