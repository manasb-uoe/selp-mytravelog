import os
from django.contrib.auth.models import User
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
    'search_base': '/mytravelog/search/'
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