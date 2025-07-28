import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
# import html_testRunner



class LoginPageTests(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.login_url = "http://127.0.0.1:8000/login/"

    def slow_type(self, element, text, delay=0.1):
        element.clear()
        for char in text:
            element.send_keys(char)
            time.sleep(delay)

    def fill_login_form_and_submit(self, username, password):
        driver = self.driver
        driver.get(self.login_url)

        # Locate input fields (check your HTML source to confirm name attributes)
        username_field = driver.find_element(By.NAME, "username")
        password_field = driver.find_element(By.NAME, "password")

        self.slow_type(username_field, username)
        self.slow_type(password_field, password)

        driver.find_element(By.CSS_SELECTOR, "form button[type='submit']").click()

    def test_empty_fields(self):
        self.fill_login_form_and_submit("", "")

        # Wait for .errorlist element (always present because of template change)
        error_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".errorlist"))
        )

        error_text = error_element.text.strip()
        self.assertTrue(
            "This field is required." in error_text,
            f"Expected 'This field is required.' but got '{error_text}'"
        )

    def test_invalid_login(self):
        self.fill_login_form_and_submit("wronguser", "wrongpass")

        error_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".errorlist"))
        )

        error_text = error_element.text.strip()
        self.assertIn(
            "Please enter a correct username and password.",
            error_text,
            f"Expected correct login error, got: '{error_text}'"
        )

    def test_valid_login(self):
        self.fill_login_form_and_submit("akash", "akash")

        # Wait for some element unique to the home page
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )

        self.assertIn("/home", self.driver.current_url)

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main(verbosity=2)