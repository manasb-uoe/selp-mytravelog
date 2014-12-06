import json
import re
from unittest.case import skip
from django.core.urlresolvers import resolve, reverse
from django.http.request import HttpRequest
from django.http.response import Http404

from django.template.loader import render_to_string
from django.test import TestCase
from mytravelog.models.city import City
from mytravelog.views.city import show_city, add_new_city, get_autocomplete_suggestions

from mytravelog.views.home import show_home


class HomeTest(TestCase):

    def test_url_resolves_to_correct_view(self):
        found = resolve('/mytravelog/')
        self.assertEqual(found.func, show_home)

    def test_if_show_home_returns_correct_html(self):
        request = HttpRequest()
        response = show_home(request)
        expected_html = render_to_string('mytravelog/home.html')
        self.assertEqual(re.sub('NOTPROVIDED', '', response.content.decode()), expected_html)


class CityTest(TestCase):

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

    def test_all_city_related_urls_resolves_to_correct_functions(self):
        found = resolve('/mytravelog/city/Test/')
        self.assertEqual(found.func, show_city)

        found = resolve('/mytravelog/city/autocomplete/')
        self.assertEqual(found.func, get_autocomplete_suggestions)

    @skip('no users registered yet')
    def test_if_show_city_returns_correct_html(self):
        # add simple city so that its name can be passed as an argument to show_city
        self.add_sample_city(self.city1_sample_data)

        request = HttpRequest()
        response = show_city(request, self.city1_sample_data['name'])
        expected_html = render_to_string('mytravelog/city.html')
        self.assertEqual(re.sub('NOTPROVIDED', '', response.content.decode()), expected_html)

    def test_saving_ranking_and_retrieving_cities(self):
        self.add_sample_city(self.city1_sample_data)
        self.add_sample_city(self.city2_sample_data)

        city1 = City.objects.get(name=self.city1_sample_data['name'])
        self.assertEqual(city1.name, self.city1_sample_data['name'])
        self.assertEqual(city1.country_name, self.city1_sample_data['country_name'])
        self.assertEqual(city1.tourist_count, self.city1_sample_data['tourist_count'])
        self.assertEqual(city1.tourist_growth, self.city1_sample_data['tourist_growth'])
        self.assertEqual(city1.description, self.city1_sample_data['description'])

        city2 = City.objects.get(name=self.city2_sample_data['name'])
        self.assertEqual(city2.name, self.city2_sample_data['name'])
        self.assertEqual(city2.country_name, self.city2_sample_data['country_name'])
        self.assertEqual(city2.tourist_count, self.city2_sample_data['tourist_count'])
        self.assertEqual(city2.tourist_growth, self.city2_sample_data['tourist_growth'])
        self.assertEqual(city2.description, self.city2_sample_data['description'])

        # city2 gets a lower rank than city1 since its tourist count is greater
        self.assertLess(city2.rank, city1.rank)

    def test_autocomplete_city_name_suggestions(self):
        # non ajax request raises 404 error
        self.assertRaises(Http404, get_autocomplete_suggestions, HttpRequest())

        # no results returned since no cities exist
        response = self.client.get('/mytravelog/city/autocomplete/',
                                   {'search_term': self.city1_sample_data['name']},
                                   'json',
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(len(json.loads(response.content)), 0)

        # this time one city should be returned since it exists in the db
        self.add_sample_city(self.city1_sample_data)
        response = self.client.get('/mytravelog/city/autocomplete/',
                                   {'search_term': self.city1_sample_data['name']},
                                   'json',
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(self.city1_sample_data['name'], json.loads(response.content)[0]['city'])
        self.assertEqual(self.city1_sample_data['country_name'], json.loads(response.content)[0]['country'])

    def add_sample_city(self, city_sample_data):
        add_new_city(name=city_sample_data['name'],
                     country_name=city_sample_data['country_name'],
                     tourist_count=city_sample_data['tourist_count'],
                     tourist_growth=city_sample_data['tourist_growth'],
                     description=city_sample_data['description'])


