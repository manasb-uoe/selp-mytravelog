import json
import re
from unittest.case import skip

from django.core.urlresolvers import resolve
from django.http.request import HttpRequest
from django.http.response import Http404

from django.template.loader import render_to_string
from django.test import TestCase

from mytravelog.models.city import City
from mytravelog.unit_tests import util
from mytravelog.views.city import show_city, get_autocomplete_suggestions

from mytravelog.views.home import show_home
from mytravelog.views.search import search_for_cities_and_users, get_search_results


class HomeTest(TestCase):

    def test_url_resolves_to_correct_view(self):
        found = resolve('/mytravelog/')
        self.assertEqual(found.func, show_home)

    def test_if_show_home_returns_correct_html(self):
        request = HttpRequest()
        response = show_home(request)
        expected_html = render_to_string('mytravelog/home.html')
        self.assertEqual(re.sub('NOTPROVIDED', '', response.content.decode()), expected_html)

    def test_if_show_home_returns_popular_cities(self):
        # add 2 sample cities and check if they are present in the returned html
        util.add_sample_city(util.city1_sample_data)
        util.add_sample_city(util.city2_sample_data)

        # check if both cities are present in the rendered template
        request = HttpRequest()
        response = show_home(request)
        response_content = response.content.decode()
        self.assertIn(util.city1_sample_data['name'], response_content)
        self.assertIn(util.city2_sample_data['name'], response_content)


class CityTest(TestCase):

    def test_all_city_related_urls_resolves_to_correct_functions(self):
        found = resolve('/mytravelog/city/Test/')
        self.assertEqual(found.func, show_city)

        found = resolve('/mytravelog/city/autocomplete/')
        self.assertEqual(found.func, get_autocomplete_suggestions)

    @skip('no users registered yet')
    def test_if_show_city_returns_correct_html(self):
        # add simple city so that its name can be passed as an argument to show_city
        util.add_sample_city(util.city1_sample_data)

        request = HttpRequest()
        response = show_city(request, util.city1_sample_data['name'])
        expected_html = render_to_string('mytravelog/city.html')
        self.assertEqual(re.sub('NOTPROVIDED', '', response.content.decode()), expected_html)

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
        response = self.client.get('/mytravelog/city/autocomplete/',
                                   {'search_term': util.city1_sample_data['name']},
                                   'json',
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(len(json.loads(response.content)), 0)

        # this time one city should be returned since it exists in the db
        util.add_sample_city(util.city1_sample_data)
        response = self.client.get('/mytravelog/city/autocomplete/',
                                   {'search_term': util.city1_sample_data['name']},
                                   'json',
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(util.city1_sample_data['name'], json.loads(response.content)[0]['city'])
        self.assertEqual(util.city1_sample_data['country_name'], json.loads(response.content)[0]['country'])


class SearchTest(TestCase):

    def test_search_url_resolves_to_correct_function(self):
        found = resolve('/mytravelog/search/')
        self.assertEqual(found.func, search_for_cities_and_users)

    @skip('no users registered yet')
    def test_search_for_cities_and_users_returns_correct_html(self):
        request = HttpRequest()
        request.GET['query'] = 'city'
        response = search_for_cities_and_users(request)
        expected_html = render_to_string('mytravelog/search.html')
        self.assertEqual(re.sub('NOTPROVIDED', '', response.content.decode()), expected_html)

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
