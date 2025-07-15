from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from ddt import ddt, data, unpack

@ddt
class UserSignupTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    @data(
        ("user1", "password123", "password123"),
        ("user2", "abcDEF123", "abcDEF123"),
        ("", "password123", "password123"),  # missing username
        ("user3", "short", "short"),         # weak password
        ("user4", "password123", "differentpassword")  # passwords don't match
    )
    @unpack
    def test_user_can_sign_up_various_inputs(self, username, password1, password2):
        self.browser.get(self.live_server_url + '/signup/')
        # fill the username field
        self.browser.find_element(By.NAME, 'username').send_keys(username)
        # fill the password1 field
        self.browser.find_element(By.NAME, 'password1').send_keys(password1)
        # fill the password2 field (password confirmation)
        self.browser.find_element(By.NAME, 'password2').send_keys(password2)
        # submit the form
        self.browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

        # Now check if signup was successful or errors shown:
        if username and password1 == password2 and len(password1) >= 8:
            # Example: After successful signup, redirect to home with welcome message
            welcome_text = self.browser.find_element(By.TAG_NAME, 'h2').text
            self.assertIn("Welcome", welcome_text)
        else:
            # There should be error messages visible for invalid inputs
            errors = self.browser.find_elements(By.CLASS_NAME, 'errorlist')
            self.assertTrue(len(errors) > 0)
