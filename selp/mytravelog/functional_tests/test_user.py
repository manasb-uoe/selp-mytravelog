import unittest
from unittest.case import skip
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

__author__ = 'Manas'


class UserTest(unittest.TestCase):

    test_username = "test_user"
    test_password = "test_password"
    url_home = 'http://127.0.0.1:8000/mytravelog/'
    url_sign_up = 'http://127.0.0.1:8000/mytravelog/sign_up/'
    url_sign_in = 'http://127.0.0.1:8000/mytravelog/sign_in/'
    url_user = 'http://127.0.0.1:8000/mytravelog/user/test_user/'

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    @skip('test_user already exists in the database')
    def test_sign_up(self):
        # User navigates to the sign up page
        self.browser.get(self.url_sign_up)

        # User notices a sign up form and tries to submit an empty form
        # an html5 input validation popup appears and user stays on the same page
        submit_button = self.browser.find_element_by_class_name('button-signup')
        submit_button.click()
        self.assertEqual(self.url_sign_up, self.browser.current_url)

        # User fills up all the fields (apart from profile picture and cover picture) and presses submit
        input_first_name = self.browser.find_element_by_name('first_name')
        input_last_name = self.browser.find_element_by_name('last_name')
        input_email = self.browser.find_element_by_name('email')
        input_username = self.browser.find_element_by_name('username')
        input_password = self.browser.find_element_by_name('password')
        input_checkbox = self.browser.find_element_by_xpath('//input[@type=\'checkbox\']')
        input_first_name.send_keys('Test')
        input_last_name.send_keys('User')
        input_email.send_keys('test_user@test.com')
        input_username.send_keys(self.test_username)
        input_password.send_keys(self.test_password)
        input_checkbox.send_keys(Keys.SPACE)
        submit_button.click()

        # User is redirected to the home page due to a successful sign up + sign in
        self.assertEqual(self.url_home, self.browser.current_url)

        # User notices their username on the navigation bar
        username_dropdown = self.browser.find_element_by_id('user-dropdown-toggle')
        self.assertEqual(self.test_username, username_dropdown.text)

    def test_sign_in_and_sign_out(self):
        # User navigates to the sign in page
        self.browser.get(self.url_sign_in)

        # User notices a sign in form and tries to submit an empty form
        # an html5 input validation popup appears and user stays on the same page
        submit_button = self.browser.find_element_by_class_name('button-signin')
        submit_button.click()
        self.assertEqual(self.url_sign_in, self.browser.current_url)

        # User fills up the username with a wrong password and presses submit
        input_username = self.browser.find_element_by_name('username')
        input_password = self.browser.find_element_by_name('password')
        input_username.send_keys(self.test_username)
        input_password.send_keys('wrong_password')
        submit_button.click()

        # The page reloads and User notices an error
        error_container = self.browser.find_element_by_class_name('alert-custom')
        self.assertIn('Incorrect username or password', error_container.text)

        # User notices that the the username they entered before pressing submit is still there in the username input
        # but password input is empty
        input_username = self.browser.find_element_by_name('username')
        input_password = self.browser.find_element_by_name('password')
        self.assertEqual(self.test_username, input_username.get_attribute('value'))
        self.assertEqual('', input_password.get_attribute('value'))

        # User fills up the correct password this time and presses submit
        input_password.send_keys(self.test_password)
        submit_button = self.browser.find_element_by_class_name('button-signin')
        submit_button.click()

        # User is redirected to the home page due to a successful sign in
        self.assertEqual(self.url_home, self.browser.current_url)

        # User notices their username on the navigation bar
        username_dropdown = self.browser.find_element_by_id('user-dropdown-toggle')
        self.assertEqual(self.test_username, username_dropdown.text)

        # User clicks on the dropdown toggle and then clicks on Sign Out menu item
        # gets redirected to the home page
        username_dropdown.click()
        user_sign_out = self.browser.find_element_by_id('user-dropdown-item-sign-out')
        user_sign_out.click()
        self.assertEqual(self.url_home, self.browser.current_url)

        # Ensure that user dropdown toggle is not visible anymore
        if len(self.browser.find_elements_by_id('user-dropdown-toggle')) != 0:
            self.fail('User dropdown should not be visible to a guest user')

    def test_user_page_tab_navigation(self):
        # User navigates to the user page
        self.browser.get(self.url_user)

        # User notices that a fragment identified for logs is immediately added to the url
        self.assertEqual(self.url_user + "#logs", self.browser.current_url)

        # User clicks on the logs tab
        # gets navigated to #logs
        link_logs = self.browser.find_element_by_css_selector('a[href=\'#logs\']')
        link_logs.click()
        self.assertEqual(self.url_user + "#logs", self.browser.current_url)

        content_divs = {
            'logs-content': self.browser.find_element_by_class_name('logs-content'),
            'albums-content': self.browser.find_element_by_class_name('albums-content'),
            'followers-content': self.browser.find_element_by_class_name('followers-content'),
            'following-content': self.browser.find_element_by_class_name('following-content')
        }
        # Check if ONLY logs content div is visible
        self.assertTrue(self.is_content_div_visible(content_divs, 'logs-content'))

        # User clicks on the albums tab
        # gets navigated to #albums and only albums content is visible
        link_albums = self.browser.find_element_by_css_selector('a[href=\'#albums\']')
        link_albums.click()
        self.assertEqual(self.url_user + "#albums", self.browser.current_url)

        # Check if ONLY albums content div is visible
        self.assertTrue(self.is_content_div_visible(content_divs, 'albums-content'))

        # User clicks on the followers tab
        # gets navigated to #followers and only followers content is visible
        link_followers = self.browser.find_element_by_css_selector('a[href=\'#followers\']')
        link_followers.click()
        self.assertEqual(self.url_user + "#followers", self.browser.current_url)

        # Check if ONLY followers content div is visible
        self.assertTrue(self.is_content_div_visible(content_divs, 'followers-content'))

        # User clicks on the following tab
        # gets navigated to #following and only following content is visible
        link_following = self.browser.find_element_by_css_selector('a[href=\'#following\']')
        link_following.click()
        self.assertEqual(self.url_user + "#following", self.browser.current_url)

        # Check if ONLY following content div is visible
        self.assertTrue(self.is_content_div_visible(content_divs, 'following-content'))

    # A helper function which checks whether a div is currently visible (while other divs are invisible)
    def is_content_div_visible(self, content_divs, content_div_classname):
        boolean_list = []
        for classname, div in content_divs.iteritems():
            if classname == content_div_classname:
                boolean_list.append('display: block' in div.get_attribute('style'))
            else:
                boolean_list.append('display: none' in div.get_attribute('style'))
        return all(boolean_list)

    def






