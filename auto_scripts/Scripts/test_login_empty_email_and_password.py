# Selenium test for TC_LOGIN_006: Both email and password fields empty
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import sys
import os

# Ensure PageClass is importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Pages')))
from LoginPage import LoginPage

class TestLoginEmptyEmailAndPassword(unittest.TestCase):
    """
    TestCase ID: TC_LOGIN_006
    Description: Attempt login with both email and password fields empty, expect validation errors 'Email is required' and 'Password is required'.
    Acceptance Criteria: Both error messages are displayed, and user remains on login page.
    """
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(5)
        self.login_page = LoginPage(self.driver)

    def test_login_with_empty_email_and_empty_password(self):
        self.login_page.go_to_login_page()
        # Leave both fields empty and click login
        self.login_page.enter_email("")
        self.login_page.enter_password("")
        self.login_page.click_login()
        # Check for both validation errors
        try:
            validation_errors = self.driver.find_elements(*self.login_page.VALIDATION_ERROR)
            error_texts = [e.text for e in validation_errors if e.is_displayed()]
            email_error = any("Email is required" in text for text in error_texts)
            password_error = any("Password is required" in text for text in error_texts)
            still_on_login_page = self.driver.current_url == self.login_page.LOGIN_URL
        except NoSuchElementException:
            email_error = False
            password_error = False
            still_on_login_page = False
        self.assertTrue(email_error, "Validation error for missing email not displayed!")
        self.assertTrue(password_error, "Validation error for missing password not displayed!")
        self.assertTrue(still_on_login_page, "User was redirected away from login page!")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
