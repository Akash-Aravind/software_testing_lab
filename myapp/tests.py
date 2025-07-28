import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import HtmlTestRunner  # Make sure to install: pip install html-testRunner
import time

class SignupPageTests(unittest.TestCase):

    def setUp(self):
        print("\n[SETUP] Launching Chrome browser...")
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.base_url = "http://127.0.0.1:8000/signup/"
        print(f"[SETUP] Base URL: {self.base_url}")

    def fill_form_and_submit(self, username, password1, password2):
        driver = self.driver
        print(f"[ACTION] Navigating to {self.base_url}")
        driver.get(self.base_url)

        print(f"[ACTION] Filling username='{username}', password1='{password1}', password2='{password2}'")
        driver.find_element(By.NAME, "username").clear()
        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "password1").clear()
        driver.find_element(By.NAME, "password1").send_keys(password1)
        driver.find_element(By.NAME, "password2").clear()
        driver.find_element(By.NAME, "password2").send_keys(password2)
        driver.find_element(By.CSS_SELECTOR, "form button").click()
        print("[ACTION] Form submitted")

    def test_empty_username(self):
        print("\n[TEST] test_empty_username started")
        self.fill_form_and_submit("", "StrongPass@123", "StrongPass@123")

        error = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".errorlist"))
        )
        print(f"[INFO] Error text found: '{error.text}'")
        self.assertIn("This field is required", error.text)

    def test_password_mismatch(self):
        print("\n[TEST] test_password_mismatch started")
        self.fill_form_and_submit("user123", "StrongPass@123", "WrongPass")

        error = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".errorlist"))
        )
        print(f"[INFO] Error text found: '{error.text}'")
        self.assertIn("The two password fields didn’t match", error.text)

    def test_all_empty(self):
        print("\n[TEST] test_all_empty started")
        self.fill_form_and_submit("", "", "")

        errors = self.driver.find_elements(By.CSS_SELECTOR, ".errorlist")
        print(f"[INFO] Number of error messages found: {len(errors)}")
        for e in errors:
            print(f"[INFO] Error: {e.text}")
        self.assertGreaterEqual(len(errors), 1)

    def tearDown(self):
        print("[TEARDOWN] Closing browser...")
        self.driver.quit()


if __name__ == "__main__":
    unittest.main(
        testRunner=HtmlTestRunner.HTMLTestRunner(output='reports'),
        verbosity=2
    )
