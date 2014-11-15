import re
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

__author__ = 'Manas'

from selenium import webdriver
import unittest


class HomeTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_home_page(self):
        # User navigates to the home page of the website
        self.browser.get('http://127.0.0.1:8000/mytravelog/')

        # User notices a search input field and a button along with it
        input_field = self.browser.find_element_by_class_name('input-city-text')
        self.assertEqual('Where do you want to go?', input_field.get_attribute('placeholder'))
        submit_button = self.browser.find_element_by_class_name('input-city-button')
        self.assertEqual('GO', submit_button.get_attribute('value'))

        # User enters a city name ('Delhi') in the input field, and clicks on submit button
        # gets navigated to the city page
        input_field.send_keys("Delhi")
        submit_button.click()
        self.assertIn("/city/Delhi/", self.browser.current_url)

        # User navigates back to the home page
        self.browser.back()

        # User enters a city name ('Delhi') in the input field, and cliks on the first autocomplete suggestion
        # gets navigated to the city page
        input_field = self.browser.find_element_by_class_name('input-city-text')
        input_field.send_keys("Delhi")
        autocomplete_suggestion = WebDriverWait(self.browser, 5).until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'suggestion')))
        autocomplete_suggestion.click()
        self.assertIn("/city/Delhi/", self.browser.current_url)

        # User navigates back to the home page
        self.browser.back()

        # User enters a city name ('Delhi') in the input field, and presses enter
        # gets navigated to the city page
        input_field = self.browser.find_element_by_class_name('input-city-text')
        input_field.send_keys("Delhi")
        input_field.send_keys(Keys.ENTER)
        self.assertIn("/city/Delhi/", self.browser.current_url)

        # User navigates back to the home page
        self.browser.back()

        # User enters the initials of a city ('D') in the input field and presses enter
        # gets navigated to search page
        input_field = self.browser.find_element_by_class_name('input-city-text')
        input_field.send_keys("D")
        input_field.send_keys(Keys.ENTER)
        self.assertIn("/search/", self.browser.current_url)

        # User navigates back to the home page
        self.browser.back()

        # User clicks on the first popular city
        # gets navigated to its city page
        popular_city_link = self.browser.find_element_by_class_name('popular-city')
        popular_city_name = self.browser.find_element_by_class_name('city-name').text
        popular_city_name = re.sub(r'\s', '_', popular_city_name)
        popular_city_link.click()
        self.assertIn("/city/" + popular_city_name + "/", self.browser.current_url)


if __name__ == '__main__':
    unittest.main()

