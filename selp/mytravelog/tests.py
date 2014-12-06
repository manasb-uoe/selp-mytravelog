import re

from django.core.urlresolvers import resolve
from django.http.request import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase

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




