import json

from django.contrib.auth.models import User
from django.core.urlresolvers import resolve
from django.http.request import HttpRequest
from django.http.response import Http404
from django.template.loader import render_to_string
from django.test import TestCase

from mytravelog.models.album import Album
from mytravelog.models.city import City
from mytravelog.models.like import Like
from mytravelog.models.log import Log
from mytravelog.models.user_profile import UserProfile
from mytravelog.unit_tests import util
from mytravelog.views.album import show_album, convert_string_to_date, create_album, update_album, delete_album
from mytravelog.views.city import show_city, get_autocomplete_suggestions
from mytravelog.views.home import show_home
from mytravelog.views.like import like_log, dislike_log
from mytravelog.views.log import create_log, edit_log, delete_log, show_log, show_live_feed
from mytravelog.views.search import search_for_cities_and_users, get_search_results
from mytravelog.views.user import sign_up, sign_in, sign_out, attach_additional_info_to_logs


class HomeTest(TestCase):

    def test_url_resolves_to_correct_view(self):
        found = resolve(util.urls['home'])
        self.assertEqual(found.func, show_home)

    def test_if_show_home_returns_correct_html(self):
        response = self.client.get(util.urls['home'])
        expected_html = render_to_string('mytravelog/home.html', {'csrf_token': self.client.cookies['csrftoken'].value})
        self.assertEqual(response.content, expected_html)

    def test_if_show_home_returns_popular_cities(self):
        # add 2 sample cities and check if they are present in the returned html
        util.add_sample_city(util.city1_sample_data)
        util.add_sample_city(util.city2_sample_data)

        # check if both cities are present in the rendered template
        response = self.client.get(util.urls['home'])
        response_content = response.content.decode()
        self.assertIn(util.city1_sample_data['name'], response_content)
        self.assertIn(util.city2_sample_data['name'], response_content)


class CityTest(TestCase):

    def test_all_city_related_urls_resolves_to_correct_functions(self):
        found = resolve(util.urls['city_base'] + 'Test' + '/')
        self.assertEqual(found.func, show_city)

        found = resolve(util.urls['city_autocomplete'])
        self.assertEqual(found.func, get_autocomplete_suggestions)

    def test_if_show_city_returns_correct_html(self):
        # add simple city so that its name can be passed as an argument to show_city
        util.add_sample_city(util.city1_sample_data)

        sample_city = City.objects.get(name=util.city1_sample_data['name'])
        response = self.client.get(util.urls['city_base'] + sample_city.url_name + '/')
        expected_html = render_to_string('mytravelog/city.html', {'requested_city': sample_city,
                                                                  'csrf_token': self.client.cookies['csrftoken'].value,
                                                                  'requested_city_logs': [],
                                                                  'current_user_albums': []})
        self.assertEqual(response.content.decode(), expected_html)

    def test_saving_ranking_and_retrieving_cities(self):
        util.add_sample_city(util.city1_sample_data)
        util.add_sample_city(util.city2_sample_data)

        city1 = City.objects.get(name=util.city1_sample_data['name'])
        self.assertEqual(city1.name, util.city1_sample_data['name'])
        self.assertEqual(city1.country_name, util.city1_sample_data['country_name'])
        self.assertEqual(city1.tourist_count, util.city1_sample_data['tourist_count'])
        self.assertEqual(city1.tourist_growth, util.city1_sample_data['tourist_growth'])
        self.assertEqual(city1.description, util.city1_sample_data['description'])

        city2 = City.objects.get(name=util.city2_sample_data['name'])
        self.assertEqual(city2.name, util.city2_sample_data['name'])
        self.assertEqual(city2.country_name, util.city2_sample_data['country_name'])
        self.assertEqual(city2.tourist_count, util.city2_sample_data['tourist_count'])
        self.assertEqual(city2.tourist_growth, util.city2_sample_data['tourist_growth'])
        self.assertEqual(city2.description, util.city2_sample_data['description'])

        # city2 gets a lower rank than city1 since its tourist count is greater
        self.assertLess(city2.rank, city1.rank)

    def test_autocomplete_city_name_suggestions(self):
        # non ajax request raises 404 error
        self.assertRaises(Http404, get_autocomplete_suggestions, HttpRequest())

        # no results returned since no cities exist
        response = self.client.get(util.urls['city_autocomplete'],
                                   {'search_term': util.city1_sample_data['name']},
                                   'json',
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(len(json.loads(response.content)), 0)

        # this time one city should be returned since it exists in the db
        util.add_sample_city(util.city1_sample_data)
        response = self.client.get(util.urls['city_autocomplete'],
                                   {'search_term': util.city1_sample_data['name']},
                                   'json',
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(util.city1_sample_data['name'], json.loads(response.content)[0]['city'])
        self.assertEqual(util.city1_sample_data['country_name'], json.loads(response.content)[0]['country'])


class SearchTest(TestCase):

    def test_search_url_resolves_to_correct_function(self):
        found = resolve(util.urls['search_base'])
        self.assertEqual(found.func, search_for_cities_and_users)

    def test_search_for_cities_and_users_returns_correct_html(self):
        response = self.client.get(util.urls['search_base'], {'query': 'city'})
        expected_html = render_to_string('mytravelog/search.html',
                                         {'csrf_token': self.client.cookies['csrftoken'].value,
                                          'user_profiles': [], 'cities': [],
                                          'results_count': 0,
                                          'query': 'city',
                                          'can_follow': False})
        self.assertEqual(response.content.decode(), expected_html)
        # print expected_html

    def test_correct_search_results_are_returned(self):
        # no cities or user profiles should be returned since they don't exist in the database yet
        results = get_search_results(util.city1_sample_data['name'])
        self.assertEqual(len(results['cities']), 0)
        self.assertEqual(len(results['user_profiles']), 0)

        # add two sample cities
        util.add_sample_city(util.city1_sample_data)
        util.add_sample_city(util.city2_sample_data)

        # if query = 'city1' then only city1 should be returned
        results = get_search_results(util.city1_sample_data['name'])
        self.assertEqual(len(results['cities']), 1)
        self.assertEqual(results['cities'][0].name, util.city1_sample_data['name'])
        self.assertEqual(len(results['user_profiles']), 0)

        # if query = 'city' then both cities should be returned
        results = get_search_results('city')
        self.assertEqual(len(results['cities']), 2)
        self.assertEqual(len(results['user_profiles']), 0)

        # TODO add user profile tests

    def test_Http404_is_raised_when_no_query_provided(self):
        request = HttpRequest()
        request.GET['query'] = 'city'
        self.assertRaises(Http404, search_for_cities_and_users, HttpRequest())


class UserAuthenticationTest(TestCase):
    def test_urls_resolve_to_current_functions(self):
        # check sign up url
        found = resolve(util.urls['sign_up'])
        self.assertEqual(found.func, sign_up)

        # check sign in url
        found = resolve(util.urls['sign_in'])
        self.assertEqual(found.func, sign_in)

        # check sign out url
        found = resolve(util.urls['sign_out'])
        self.assertEqual(found.func, sign_out)

    def test_views_return_correct_html(self):
        # check sign_up view
        response = self.client.get(util.urls['sign_up'])
        expected_html = render_to_string('mytravelog/sign_up.html', {'csrf_token': self.client.cookies['csrftoken'].value})
        self.assertEqual(response.content, expected_html)

        # check sign_in view
        response = self.client.get(util.urls['sign_in'])
        expected_html = render_to_string('mytravelog/sign_in.html', {'csrf_token': self.client.cookies['csrftoken'].value})
        self.assertEqual(response.content, expected_html)

    def test_sign_out_view_redirects_anonymous_users_to_sign_in(self):
        response = self.client.get(util.urls['sign_out'], None, follow=True)
        self.assertRedirects(response, util.urls['sign_in'], status_code=302, target_status_code=200)

    def test_sign_in_and_sign_up_views_redirect_authenticated_users_to_their_profiles(self):
        # create and sign in a new user
        util.add_sample_user_and_user_profile(util.user1_sample_data)
        is_successful = self.client.login(username=util.user1_sample_data['username'],
                                          password=util.user1_sample_data['password'])
        self.assertTrue(is_successful)

        # auth user gets redirected to user profile page if they try to sign in or sign up
        response = self.client.post(util.urls['sign_in'], util.user1_sample_data, follow=True)
        self.assertRedirects(response, util.urls['user_base'] + util.user1_sample_data['username'] + '/', status_code=302, target_status_code=200)
        self.client.post(util.urls['sign_up'], util.user1_sample_data, follow=True)
        self.assertRedirects(response, util.urls['user_base'] + util.user1_sample_data['username'] + '/', status_code=302, target_status_code=200)

    def test_sign_up_creates_new_user_and_user_profile(self):
        # on success, a new user and user profile should be created and the user should get redirected to user page
        response = self.client.post(util.urls['sign_up'], util.user1_sample_data, follow=True)
        self.assertRedirects(response, util.urls['user_base'] + util.user1_sample_data['username'] + '/', status_code=302, target_status_code=200)
        new_user = User.objects.get(username=util.user1_sample_data['username'])
        new_user_profile = UserProfile.objects.get(user=new_user)

        # check if all saved data are correct
        self.assertEqual(new_user.username, util.user1_sample_data['username'])
        self.assertEqual(new_user.first_name, util.user1_sample_data['first_name'])
        self.assertEqual(new_user.last_name, util.user1_sample_data['last_name'])
        self.assertEqual(new_user_profile.city_count, 0)
        self.assertEqual(new_user_profile.country_count, 0)
        self.assertEqual(new_user_profile.rank, -1)

    def test_sign_in_view_logs_in_registered_user(self):
        # a user that has never registered before gets an error saying 'Incorrect username or password'
        response = self.client.post(util.urls['sign_in'], util.user1_sample_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['error'], 'Incorrect username or password')

        # an already registered user should get signed in and be redirected to user page
        util.add_sample_user_and_user_profile(util.user1_sample_data)
        response = self.client.post(util.urls['sign_in'], util.user1_sample_data, follow=True)
        self.assertRedirects(response, util.urls['user_base'] + util.user1_sample_data['username'] + '/', status_code=302, target_status_code=200)

    def test_sign_out_view_signs_out_an_authenticated_user(self):
        util.add_sample_user_and_user_profile(util.user1_sample_data)
        is_successful = self.client.login(username=util.user1_sample_data['username'],
                                          password=util.user1_sample_data['password'])
        self.assertTrue(is_successful)

    def test_sign_up_validation(self):
        # test all possible validation errors (including uploaded file size errors)
        user_data_dict = {}
        response = self.client.post(util.urls['sign_up'], user_data_dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['error'], 'First name is required')

        user_data_dict['first_name'] = util.user1_sample_data['first_name']
        response = self.client.post(util.urls['sign_up'], user_data_dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['error'], 'Last name is required')

        user_data_dict['last_name'] = util.user1_sample_data['last_name']
        response = self.client.post(util.urls['sign_up'], user_data_dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['error'], 'Email is required')

        user_data_dict['email'] = 'email'
        response = self.client.post(util.urls['sign_up'], user_data_dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['error'], 'Email is missing the \'@\' symbol')

        user_data_dict['email'] = util.user1_sample_data['email']
        response = self.client.post(util.urls['sign_up'], user_data_dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['error'], 'Username is required')

        user_data_dict['username'] = 'user'
        response = self.client.post(util.urls['sign_up'], user_data_dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['error'], 'Username must be at least 6 characters long')

        user_data_dict['username'] = 'user user'
        response = self.client.post(util.urls['sign_up'], user_data_dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['error'], 'Username cannot contain spaces')

        user_data_dict['username'] = util.user1_sample_data['username']
        response = self.client.post(util.urls['sign_up'], user_data_dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['error'], 'Password is required')

        user_data_dict['password'] = 'pass'
        response = self.client.post(util.urls['sign_up'], user_data_dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['error'], 'Password must be at least 6 characters long')

        user_data_dict['password'] = util.user1_sample_data['password']
        user_data_dict['profile_picture'] = util.get_large_image()
        response = self.client.post(util.urls['sign_up'], user_data_dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['error'], 'Max image size allowed is 2 mb')

        user_data_dict['profile_picture'] = util.get_small_image()
        user_data_dict['cover_picture'] = util.get_large_image()
        response = self.client.post(util.urls['sign_up'], user_data_dict)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['error'], 'Max image size allowed is 2 mb')

        user_data_dict['cover_picture'] = util.get_small_image()
        response = self.client.post(util.urls['sign_up'], user_data_dict, follow=True)

        # now that all data is validated, user should be successfully signed up and redirected to user page
        self.assertRedirects(response,
                             util.urls['user_base'] + util.user1_sample_data['username'] + '/',
                             status_code=302,
                             target_status_code=200)

        # sign out and try to create a new user with the same username
        self.client.logout()
        response = self.client.post(util.urls['sign_up'], {'first_name': util.user1_sample_data['first_name'],
                                                           'last_name': util.user1_sample_data['last_name'],
                                                           'email': util.user1_sample_data['email'],
                                                           'username': util.user1_sample_data['username'],
                                                           'password': util.user1_sample_data['password'],
                                                           'profile_picture': util.get_small_image(),
                                                           'cover_picture': util.get_small_image()}, follow=True)
        self.assertEqual(response.context['error'], 'That username is not available')


class AlbumTest(TestCase):

    def test_urls_resolve_to_correct_functions(self):
        # check show album url
        found = resolve(util.urls['album_show_base'] + '0/')
        self.assertEqual(found.func, show_album)

        # check create album url
        found = resolve(util.urls['album_create'])
        self.assertEqual(found.func, create_album)

        # check update album url
        found = resolve(util.urls['album_update_base'] + '0/')
        self.assertEqual(found.func, update_album)

        # check delete album url
        found = resolve(util.urls['album_delete_base'] + '0/')
        self.assertEqual(found.func, delete_album)

    def test_show_album_view_returns_correct_html(self):
        # add a new album since show_album view needs an id
        util.add_sample_user_and_user_profile(util.user1_sample_data)
        util.add_sample_album(util.album1_sample_data, util.user1_sample_data)
        album = util.get_album(util.album1_sample_data, util.user1_sample_data)
        user_dict = util.get_user_and_user_profile(util.user1_sample_data)
        user = user_dict['user']
        user_profile = user_dict['user_profile']

        response = self.client.get(util.urls['album_show_base'] + str(album.id) + '/')
        expected_html = render_to_string('mytravelog/user_album.html',
                                         {'csrf_token': self.client.cookies['csrftoken'].value,
                                          'requested_album': album,
                                          'requested_user_albums': [album],
                                          'requested_album_logs': [],
                                          'requested_user': user,
                                          'requested_user_profile': user_profile,
                                          'can_follow': False,
                                          'can_edit_profile': False})

        self.assertEqual(response.content.decode(), expected_html)

    def test_create_album_view(self):
        # non ajax request raises 404 error
        self.assertRaises(Http404, create_album, HttpRequest())
        # anon user gets redirected to sign in page
        response = self.client.post(util.urls['album_create'],
                                    data=util.album1_sample_data,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(json.loads(response.content)['redirect_to'], util.urls['sign_in'])

        # create and sign in a new user
        util.add_sample_user_and_user_profile(util.user1_sample_data)
        is_successful = self.client.login(username=util.user1_sample_data['username'],
                                          password=util.user1_sample_data['password'])
        self.assertTrue(is_successful)

        # as the user is now authenticated, album should be created successfully
        self.client.post(util.urls['album_create'],
                         data=util.album1_sample_data,
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # check if all saved data are correct
        album = util.get_album(util.album1_sample_data, util.user1_sample_data)
        self.assertEqual(album.name, util.album1_sample_data['name'])
        self.assertEqual(album.start_date, convert_string_to_date(util.album1_sample_data['start_date']))
        self.assertEqual(album.end_date, convert_string_to_date(util.album1_sample_data['end_date']))

    def test_update_album_view(self):
        # create and retrieve an album to be edited
        util.add_sample_user_and_user_profile(util.user1_sample_data)
        util.add_sample_album(util.album1_sample_data, util.user1_sample_data)
        album = util.get_album(util.album1_sample_data, util.user1_sample_data)

        # non ajax request raises 404 error
        response = self.client.post(util.urls['album_update_base'] + str(album.id) + '/',
                                    data=util.album2_sample_data)
        self.assertEqual(response.status_code, 404)

        # anon user gets redirected to sign in page
        response = self.client.post(util.urls['album_update_base'] + str(album.id) + '/',
                                    data=util.album2_sample_data,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(json.loads(response.content)['redirect_to'], util.urls['sign_in'])

        # sign in user
        is_successful = self.client.login(username=util.user1_sample_data['username'],
                                          password=util.user1_sample_data['password'])
        self.assertTrue(is_successful)

        # as the user is now authenticated, album should be updated successfully
        self.client.post(util.urls['album_update_base'] + str(album.id) + '/',
                         data=util.album2_sample_data,
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # check if all saved data are correct
        album = util.get_album(util.album2_sample_data, util.user1_sample_data)
        self.assertEqual(album.name, util.album2_sample_data['name'])
        self.assertEqual(album.start_date, convert_string_to_date(util.album2_sample_data['start_date']))
        self.assertEqual(album.end_date, convert_string_to_date(util.album2_sample_data['end_date']))

    def test_delete_album_view(self):
        # create and retrieve an album to be delete
        util.add_sample_user_and_user_profile(util.user1_sample_data)
        util.add_sample_album(util.album1_sample_data, util.user1_sample_data)
        album = util.get_album(util.album1_sample_data, util.user1_sample_data)

        # non ajax request raises 404 error
        response = self.client.post(util.urls['album_delete_base'] + str(album.id) + '/',
                                    data=util.album1_sample_data)
        self.assertEqual(response.status_code, 404)

        # anon user gets redirected to sign in page
        response = self.client.post(util.urls['album_delete_base'] + str(album.id) + '/',
                                    data=util.album1_sample_data,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(json.loads(response.content)['redirect_to'], util.urls['sign_in'])

        # sign in user
        is_successful = self.client.login(username=util.user1_sample_data['username'],
                                          password=util.user1_sample_data['password'])
        self.assertTrue(is_successful)

        # as the user is now authenticated, album should be deleted successfully
        self.client.post(util.urls['album_update_base'] + str(album.id) + '/',
                         data=util.album2_sample_data,
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # check if album was actually deleted
        self.assertEqual(len(Album.objects.filter(name=util.album1_sample_data['name'],
                                                  user_profile__user__username=util.user1_sample_data['username'])), 0)

    def test_album_form_validation(self):
        # create and sign in a new user
        util.add_sample_user_and_user_profile(util.user1_sample_data)
        is_successful = self.client.login(username=util.user1_sample_data['username'],
                                          password=util.user1_sample_data['password'])
        self.assertTrue(is_successful)

        # as the user is now authenticated, we can start our validation checks with an empty dict passed to create_album
        album_data_dict = {

        }
        response = self.client.post(util.urls['album_create'],
                                    data=album_data_dict,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(json.loads(response.content)['error'], "Album name is required")

        album_data_dict['name'] = 'None'
        response = self.client.post(util.urls['album_create'],
                                    data=album_data_dict,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(json.loads(response.content)['error'], "Album name cannot be 'None'")

        album_data_dict['name'] = util.album1_sample_data['name']
        response = self.client.post(util.urls['album_create'],
                                    data=album_data_dict,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(json.loads(response.content)['error'], "Start date is required")

        album_data_dict['start_date'] = util.album1_sample_data['start_date']
        response = self.client.post(util.urls['album_create'],
                                    data=album_data_dict,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(json.loads(response.content)['error'], "End date is required")

        album_data_dict['end_date'] = '1900-1-1'
        response = self.client.post(util.urls['album_create'],
                                    data=album_data_dict,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(json.loads(response.content)['error'], "End date must come after Start date")

        album_data_dict['end_date'] = util.album1_sample_data['end_date']
        cover_picture = util.get_large_image()
        album_data_dict['cover_picture'] = cover_picture
        response = self.client.post(util.urls['album_create'],
                                    data=album_data_dict,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(json.loads(response.content)['error'], "Max image size allowed is 2 mb")

        cover_picture = util.get_small_image()
        album_data_dict['cover_picture'] = cover_picture
        response = self.client.post(util.urls['album_create'],
                                    data=album_data_dict,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(len(json.loads(response.content)), 0)

        # now try to create another album with the same name
        album_data_dict['cover_picture'] = cover_picture
        response = self.client.post(util.urls['album_create'],
                                    data=album_data_dict,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(json.loads(response.content)['error'], "You already have an album with the same name")


class LogTest(TestCase):

    def test_urls_resolve_to_correct_functions(self):
        # check create log url
        found = resolve(util.urls['log_create'])
        self.assertEqual(found.func, create_log)

        # check update log url
        found = resolve(util.urls['log_update_base'] + '0/')
        self.assertEqual(found.func, edit_log)

        # check delete log url
        found = resolve(util.urls['log_delete_base'] + '0/')
        self.assertEqual(found.func, delete_log)

        # check show log url
        found = resolve(util.urls['log_show_base'] + '0/')
        self.assertEqual(found.func, show_log)

    def test_show_log_view_returns_correct_html(self):
        # log data to be used for log creation
        log_sample_data = util.log1_sample_data
        log_sample_data['log_picture_1'] = util.get_small_image()
        log_sample_data['location'] = util.city1_sample_data['name']
        log_sample_data['album_name'] = util.album1_sample_data['name']

        # first we need to create a log since show_album needs a log id
        util.add_sample_city(util.city1_sample_data)
        util.add_sample_user_and_user_profile(util.user1_sample_data)
        util.add_sample_album(util.album1_sample_data, util.user1_sample_data)
        util.add_sample_log(util.log1_sample_data, util.album1_sample_data, util.city1_sample_data, util.user1_sample_data)

        album = util.get_album(util.album1_sample_data, util.user1_sample_data)
        log = attach_additional_info_to_logs(Log.objects.all(), None)

        # get user and user profile
        user_dict = util.get_user_and_user_profile(util.user1_sample_data)
        user = user_dict['user']
        user_profile = user_dict['user_profile']

        response = self.client.get(util.urls['log_show_base'] + str(log[0].id) + '/')
        expected_html = render_to_string('mytravelog/user_log.html',
                                         {'csrf_token': self.client.cookies['csrftoken'].value,
                                          'requested_log': log,
                                          'requested_user_albums': [album],
                                          'requested_user': user,
                                          'requested_user_profile': user_profile,
                                          'can_follow': False,
                                          'can_edit_profile': False})

        self.assertEqual(response.content.decode(), expected_html)

    def test_create_log_view(self):
        # log data to be used for log creation
        log_sample_data = util.log1_sample_data
        log_sample_data['log_picture_1'] = util.get_small_image()
        log_sample_data['location'] = util.city1_sample_data['name']
        log_sample_data['album_name'] = util.album1_sample_data['name']

        # non ajax request raises 404 error
        self.assertRaises(Http404, create_log, HttpRequest())
        # anon user gets redirected to sign in page
        response = self.client.post(util.urls['log_create'],
                                    data=log_sample_data,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(json.loads(response.content)['redirect_to'], util.urls['sign_in'])

        # create and sign in a new user
        util.add_sample_user_and_user_profile(util.user1_sample_data)
        is_successful = self.client.login(username=util.user1_sample_data['username'],
                                          password=util.user1_sample_data['password'])
        self.assertTrue(is_successful)

        # before we can create a lot, we must add a city and album with the log belongs to
        util.add_sample_city(util.city1_sample_data)
        util.add_sample_album(util.album1_sample_data, util.user1_sample_data)

        # as the user is now authenticated, album should be created successfully
        self.client.post(util.urls['log_create'],
                         data=log_sample_data,
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # check if all saved data is correct
        log = Log.objects.all()
        self.assertEqual(len(log), 1)
        log = log[0]
        self.assertEqual(log.album.name, log_sample_data['album_name'])
        self.assertEqual(log.city.name, log_sample_data['location']),
        self.assertEqual(log.latitude, log_sample_data['latitude'])
        self.assertEqual(log.longitude, log_sample_data['longitude'])
        self.assertEqual(log.description, log_sample_data['description'])
        self.assertEqual(log.user_profile.user.username, util.user1_sample_data['username'])

    def test_update_log_view(self):
        # log data to be used for log creation
        log_sample_data = util.log2_sample_data
        log_sample_data['log_picture_1'] = util.get_small_image()
        log_sample_data['location'] = util.city1_sample_data['name']
        log_sample_data['album_name'] = util.album1_sample_data['name']

        # first we need to create a log since update_log view needs a log id
        util.add_sample_city(util.city1_sample_data)
        util.add_sample_user_and_user_profile(util.user1_sample_data)
        util.add_sample_album(util.album1_sample_data, util.user1_sample_data)
        util.add_sample_log(util.log2_sample_data, util.album1_sample_data, util.city1_sample_data, util.user1_sample_data)

        log = Log.objects.all()[0]

        # non ajax request raises 404 error
        response = self.client.post(util.urls['log_update_base'] + str(log.id) + '/',
                                    data=log_sample_data)
        self.assertEqual(response.status_code, 404)

        # anon user gets redirected to sign in page
        response = self.client.post(util.urls['log_update_base'] + str(log.id) + '/',
                                    data=log_sample_data,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(json.loads(response.content)['redirect_to'], util.urls['sign_in'])

        # sign in user
        is_successful = self.client.login(username=util.user1_sample_data['username'],
                                          password=util.user1_sample_data['password'])
        self.assertTrue(is_successful)

        # as the user is now authenticated, log should be updated successfully
        self.client.post(util.urls['log_update_base'] + str(log.id) + '/',
                         data=log_sample_data,
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # check if all saved data are correct
        updated_log = Log.objects.all()[0]
        self.assertEqual(updated_log.album.name, log_sample_data['album_name'])
        self.assertEqual(updated_log.city.name, log_sample_data['location']),
        self.assertEqual(updated_log.latitude, log_sample_data['latitude'])
        self.assertEqual(updated_log.longitude, log_sample_data['longitude'])
        self.assertEqual(updated_log.description, log_sample_data['description'])
        self.assertEqual(updated_log.user_profile.user.username, util.user1_sample_data['username'])

    def test_delete_album_view(self):
        # log data to be used for log creation
        log_sample_data = util.log1_sample_data
        log_sample_data['log_picture_1'] = util.get_small_image()
        log_sample_data['location'] = util.city1_sample_data['name']
        log_sample_data['album_name'] = util.album1_sample_data['name']

        # first we need to create a log since update_log view needs a log id
        util.add_sample_city(util.city1_sample_data)
        util.add_sample_user_and_user_profile(util.user1_sample_data)
        util.add_sample_album(util.album1_sample_data, util.user1_sample_data)
        util.add_sample_log(util.log1_sample_data, util.album1_sample_data, util.city1_sample_data, util.user1_sample_data)

        log = Log.objects.all()[0]

        # non ajax request raises 404 error
        response = self.client.post(util.urls['log_delete_base'] + str(log.id) + '/',
                                    data=log_sample_data)
        self.assertEqual(response.status_code, 404)

        # anon user gets redirected to sign in page
        response = self.client.post(util.urls['log_delete_base'] + str(log.id) + '/',
                                    data=log_sample_data,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(json.loads(response.content)['redirect_to'], util.urls['sign_in'])

        # sign in user
        is_successful = self.client.login(username=util.user1_sample_data['username'],
                                          password=util.user1_sample_data['password'])
        self.assertTrue(is_successful)

        # as the user is now authenticated, log should be deleted successfully
        self.client.post(util.urls['log_delete_base'] + str(log.id) + '/',
                         data=log_sample_data,
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(len(Log.objects.all()), 0)

    def test_get_log_info_for_map_view(self):
        # log data to be used for log creation
        log_sample_data = util.log1_sample_data
        log_sample_data['log_picture_1'] = util.get_small_image()
        log_sample_data['location'] = util.city1_sample_data['name']
        log_sample_data['album_name'] = util.album1_sample_data['name']

        # first we need to create a log since get_log_info_for_map returns all logs for a particular user
        util.add_sample_city(util.city1_sample_data)
        util.add_sample_user_and_user_profile(util.user1_sample_data)
        util.add_sample_album(util.album1_sample_data, util.user1_sample_data)
        util.add_sample_log(util.log1_sample_data, util.album1_sample_data, util.city1_sample_data, util.user1_sample_data)

        user = util.get_user_and_user_profile(util.user1_sample_data)['user']

        # non ajax request raises 404 error
        response = self.client.get(util.urls['log_get_info_for_map_base'] + user.username + '/')
        self.assertEqual(response.status_code, 404)

        # since get_log_info_for_map doesn't require a user to be authenticated, it should now return all logs belonging
        # to the provided username
        response = self.client.get(util.urls['log_get_info_for_map_base'] + user.username + '/',
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        log = Log.objects.all()[0]
        response_dict = json.loads(response.content)['user_logs_info'][str(log.id)]
        self.assertEqual(response_dict['city'], log.city.name)
        self.assertEqual(response_dict['date_and_time'], str(log.created_at))
        self.assertEqual(response_dict['latitude'], str(log.latitude))
        self.assertEqual(response_dict['longitude'], str(log.longitude))
        self.assertEqual(response_dict['url'], '/mytravelog/log/' + str(log.id) + '/')

    def test_log_form_validation(self):
        # create and sign in a new user
        util.add_sample_user_and_user_profile(util.user1_sample_data)
        is_successful = self.client.login(username=util.user1_sample_data['username'],
                                          password=util.user1_sample_data['password'])
        self.assertTrue(is_successful)

        # before we can create a lot, we must add a city and album with the log belongs to
        util.add_sample_city(util.city1_sample_data)
        util.add_sample_album(util.album1_sample_data, util.user1_sample_data)

        # as the user is now authenticated, we can start our validation checks with an empty dict passed to create_log
        log_data_dict = {}
        response = self.client.post(util.urls['log_create'],
                                    data=log_data_dict,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(json.loads(response.content)['error'], "Your location could not be verified")

        log_data_dict['location'] = util.city1_sample_data['name']
        log_data_dict['latitude'] = util.log1_sample_data['latitude']
        log_data_dict['longitude'] = util.log1_sample_data['longitude']
        response = self.client.post(util.urls['log_create'],
                                    data=log_data_dict,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(json.loads(response.content)['error'], "Description is required")

        long_description = ''
        while len(long_description) < 1001:
            long_description += 'd'
        log_data_dict['description'] = long_description
        response = self.client.post(util.urls['log_create'],
                                    data=log_data_dict,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(json.loads(response.content)['error'], "Description length cannot exceed 1000 characters")

        log_data_dict['description'] = util.log1_sample_data['description']
        response = self.client.post(util.urls['log_create'],
                                    data=log_data_dict,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(json.loads(response.content)['error'], "At least one image is required")

        log_data_dict['log_picture_1'] = util.get_large_image()
        response = self.client.post(util.urls['log_create'],
                                    data=log_data_dict,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(json.loads(response.content)['error'], "Max image size allowed is 2 mb")

        log_data_dict['log_picture_1'] = util.get_small_image()
        fake_city_name = 'not a city'
        log_data_dict['location'] = fake_city_name
        response = self.client.post(util.urls['log_create'],
                                    data=log_data_dict,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(json.loads(response.content)['error'], "No city named '" + fake_city_name + "' in the database")

        log_data_dict['location'] = util.city1_sample_data['name']
        counter = 1
        while counter < 12:
            log_data_dict['log_picture_' + str(counter)] = util.get_small_image()
            counter += 1
        response = self.client.post(util.urls['log_create'],
                                    data=log_data_dict,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(json.loads(response.content)['error'], "At most 10 images are allowed")

        # now that all validation checks have tested, try to create a log with valid data
        log_data_dict = util.log1_sample_data
        log_data_dict['log_picture_1'] = util.get_small_image()
        log_data_dict['location'] = util.city1_sample_data['name']
        log_data_dict['album_name'] = util.album1_sample_data['name']
        response = self.client.post(util.urls['log_create'],
                                    data=log_data_dict,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # as all validation checks have been passed, no errors should be returned
        self.assertEqual(len(json.loads(response.content)), 0)


class LikeTest(TestCase):

    def test_create_and_delete_like_urls_resolve_to_correct_functions(self):
        found = resolve(util.urls['like_create_base'] + '0/')
        self.assertEqual(found.func, like_log)

        found = resolve(util.urls['like_delete_base'] + '0/')
        self.assertEqual(found.func, dislike_log)

    def test_like_log_view(self):
        # first we need to create a log since like_log view needs a log id as an argument
        util.add_sample_city(util.city1_sample_data)
        util.add_sample_user_and_user_profile(util.user1_sample_data)
        util.add_sample_album(util.album1_sample_data, util.user1_sample_data)
        util.add_sample_log(util.log1_sample_data, util.album1_sample_data, util.city1_sample_data, util.user1_sample_data)

        log_to_like = Log.objects.all()[0]

        # non ajax request raises 404 error
        response = self.client.post(util.urls['like_create_base'] + str(log_to_like.id) + '/')
        self.assertEqual(response.status_code, 404)

        # anon user gets redirected to sign in page
        response = self.client.post(util.urls['like_create_base'] + str(log_to_like.id) + '/',
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(json.loads(response.content)['redirect_to'], util.urls['sign_in'])

        # sign in the user we just created
        is_successful = self.client.login(username=util.user1_sample_data['username'],
                                          password=util.user1_sample_data['password'])
        self.assertTrue(is_successful)

        # as the user is now authenticated, like should be created successfully
        self.client.post(util.urls['like_create_base'] + str(log_to_like.id) + '/',
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(len(Like.objects.filter(log=log_to_like)), 1)

        # if we try to create the same like again, it should not be created since one user can only like a log once
        self.client.post(util.urls['like_create_base'] + str(log_to_like.id) + '/',
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(len(Like.objects.filter(log=log_to_like)), 1)

    def test_dislike_log_view(self):
        # first we need to create a log since dislike_log view needs a log id as an argument
        util.add_sample_city(util.city1_sample_data)
        util.add_sample_user_and_user_profile(util.user1_sample_data)
        util.add_sample_album(util.album1_sample_data, util.user1_sample_data)
        util.add_sample_log(util.log1_sample_data, util.album1_sample_data, util.city1_sample_data, util.user1_sample_data)

        # now we need to create a like which needs to be deleted
        log_to_dislike = Log.objects.all()[0]
        liker_user_profile = util.get_user_and_user_profile(util.user1_sample_data)['user_profile']
        Like.objects.create(log=log_to_dislike, liker_user_profile=liker_user_profile)
        self.assertEqual(len(Like.objects.filter(log=log_to_dislike)), 1)

        # non ajax request raises 404 error
        response = self.client.post(util.urls['like_delete_base'] + str(log_to_dislike.id) + '/')
        self.assertEqual(response.status_code, 404)

        # anon user gets redirected to sign in page
        response = self.client.post(util.urls['like_delete_base'] + str(log_to_dislike.id) + '/',
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(json.loads(response.content)['redirect_to'], util.urls['sign_in'])

        # sign in the user we just created
        is_successful = self.client.login(username=util.user1_sample_data['username'],
                                          password=util.user1_sample_data['password'])
        self.assertTrue(is_successful)

        # as the user is now authenticated, like should be deleted successfully
        self.client.post(util.urls['like_delete_base'] + str(log_to_dislike.id) + '/',
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(len(Like.objects.filter(log=log_to_dislike)), 0)

        # if we try to delete the same like again, error should not be raised
        self.client.post(util.urls['like_delete_base'] + str(log_to_dislike.id) + '/',
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(len(Like.objects.filter(log=log_to_dislike)), 0)
        self.assertEqual(response.status_code, 200)

