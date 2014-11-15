import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

__author__ = 'Manas'


class NavigationBarTest(unittest.TestCase):

    admin_username = 'enthusiast94'
    admin_password = '123123'

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_links_as_guest(self):
        # User navigates to the home page of the website
        # (although navigation bar can be tested from any page, as it is included in the master template)
        self.browser.get('http://127.0.0.1:8000/mytravelog/')

        # User clicks on brand name (website name)
        # gets navigated to the home page
        brand_name = self.browser.find_element_by_class_name('navbar-brand')
        brand_name.click()

        # User clicks on Sign In
        # gets navigated to the sign in page
        sign_in = self.browser.find_element_by_class_name('a-signin')
        sign_in.click()
        self.assertIn('/sign_in/', self.browser.current_url)

        # User clicks on Sign Up
        # gets navigated to the sign up page
        sign_up = self.browser.find_element_by_class_name('a-signup')
        sign_up.click()
        self.assertIn('/sign_up/', self.browser.current_url)

        # Ensure that user dropdown toggle is not visible in guest mode
        if len(self.browser.find_elements_by_id('user-dropdown-toggle')) != 0:
            self.fail('User dropdown should not be visible to a guest user')

    def test_links_as_authenticated_user(self):
        # User navigates to the home page of the website
        # (although navigation bar can be tested from any page, as it is included in the master template)
        self.browser.get('http://127.0.0.1:8000/mytravelog/')

        # User decides to sign in using the admin account
        sign_in = self.browser.find_element_by_class_name('a-signin')
        sign_in.click()
        username_input = WebDriverWait(self.browser, 5).until(expected_conditions.visibility_of_element_located((By.NAME, 'username')))
        username_input.send_keys(self.admin_username)
        password_input = self.browser.find_element_by_name('password')
        # Ensure that the password is not visible
        self.assertEqual('password', password_input.get_attribute('type'))
        password_input.send_keys(self.admin_password)
        submit_button = self.browser.find_element_by_class_name('button-signin')
        submit_button.click()

        # User is redirected to the home page due to a successful sign in
        self.assertEqual('http://127.0.0.1:8000/mytravelog/', self.browser.current_url)

        # User notices their username on the navigation bar
        username_dropdown = self.browser.find_element_by_id('user-dropdown-toggle')
        self.assertEqual(self.admin_username, username_dropdown.text)

        # User clicks on the dropdown toggle with their username on it, and then clicks on View Profile menu item
        # gets navigated to the user page
        username_dropdown.click()
        user_view_profile = self.browser.find_element_by_id('user-dropdown-item-view-profile')
        user_view_profile.click()
        self.assertIn('/user/' + self.admin_username + '/', self.browser.current_url)

        # User clicks on the dropdown toggle again, and then clicks on Sign Out menu item
        # gets redirected to the home page
        username_dropdown = self.browser.find_element_by_id('user-dropdown-toggle')
        username_dropdown.click()
        user_sign_out = self.browser.find_element_by_id('user-dropdown-item-sign-out')
        user_sign_out.click()
        self.assertEqual('http://127.0.0.1:8000/mytravelog/', self.browser.current_url)

        # Ensure that user dropdown toggle is not visible anymore
        if len(self.browser.find_elements_by_id('user-dropdown-toggle')) != 0:
            self.fail('User dropdown should not be visible to a guest user')

if __name__ == '__main__':
    unittest.main()

