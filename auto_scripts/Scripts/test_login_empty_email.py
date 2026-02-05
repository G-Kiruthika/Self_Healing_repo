# Selenium Python Automation Test Script for TC_LOGIN_003
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage
import time

class TestLoginEmptyEmail(unittest.TestCase):
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=chrome_options)
        self.login_page = LoginPage(self.driver)

    def tearDown(self):
        self.driver.quit()

    def test_login_with_empty_email(self):
        """
        TC_LOGIN_003: Attempt login with empty email and valid password
        Steps:
        1. Navigate to login page
        2. Leave email field empty
        3. Enter valid password
        4. Click Login
        5. Verify validation error and login prevented
        """
        # Step 1: Navigate to login page
        result = self.login_page.navigate_to_login()
        self.assertTrue(result, "Login page should be displayed.")

        # Step 2: Leave email field empty
        email_empty = self.login_page.leave_email_field_empty()
        self.assertTrue(email_empty, "Email field should remain empty.")

        # Step 3: Enter valid password
        valid_password = "ValidPass123!"
        password_ok = self.login_page.enter_valid_password(valid_password)
        self.assertTrue(password_ok, "Password should be masked and accepted.")

        # Step 4: Click Login
        validation_error = self.login_page.click_login_for_empty_email()
        self.assertTrue(validation_error, "Validation error 'Email is required' should be displayed.")

        # Step 5: Verify login is prevented and user remains on login page
        login_prevented = self.login_page.verify_login_prevented()
        self.assertTrue(login_prevented, "User should remain on login page and not be authenticated.")

if __name__ == "__main__":
    unittest.main()
