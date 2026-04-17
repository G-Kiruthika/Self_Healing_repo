"""
Test Script for TC-LOGIN-005: Login with empty password field
Author: Automation Generator
Traceability: Maps to testCaseId=232, testCaseDescription='Test Case TC-LOGIN-005'

This script validates that attempting to login with a valid email but empty password results in a validation error and does not authenticate the user.
"""
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
import sys
import os
import time

# Ensure Pages directory is importable
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PAGES_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '../Pages'))
sys.path.insert(0, PAGES_DIR)

from TC_LOGIN_005_TestPage import TC_LOGIN_005_TestPage

class TestTCLogin005(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        try:
            cls.driver = webdriver.Chrome(options=chrome_options)
        except WebDriverException as e:
            raise RuntimeError(f"WebDriver initialization failed: {e}")
        cls.page = TC_LOGIN_005_TestPage(cls.driver)
        cls.test_email = "testuser@example.com"
        cls.login_url = "https://ecommerce.example.com/login"

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_login_with_empty_password(self):
        """
        Steps:
        1. Navigate to login page
        2. Enter valid email
        3. Leave password field empty
        4. Click Login
        5. Assert validation error
        6. Assert user remains on login page
        """
        # Step 1: Navigate to login page
        self.page.go_to_login_page(self.login_url)
        self.assertTrue(self.page.is_on_login_page(), "Login page should be displayed.")

        # Step 2: Enter valid email
        self.page.enter_email(self.test_email)
        # Assert email field contains the entered value
        email_input = self.page.driver.find_element_by_id(self.page.email_field.split('=',1)[1])
        self.assertEqual(email_input.get_attribute('value'), self.test_email, "Email should be entered correctly.")

        # Step 3: Leave password field empty
        self.page.leave_password_empty()
        password_input = self.page.driver.find_element_by_id(self.page.password_field.split('=',1)[1])
        self.assertEqual(password_input.get_attribute('value'), '', "Password field should remain blank.")

        # Step 4: Click Login
        self.page.click_login()
        time.sleep(1)  # Allow UI to update error message

        # Step 5: Assert validation error is displayed
        error_text = self.page.get_validation_error()
        self.assertIsNotNone(error_text, "Validation error should be displayed for empty password.")
        self.assertTrue(
            'password is required' in error_text.lower() or 'please fill in all required fields' in error_text.lower(),
            f"Validation error message should indicate missing password. Actual: {error_text}"
        )

        # Step 6: Assert user remains on login page
        self.assertTrue(self.page.is_on_login_page(), "User should remain on login page without authentication.")

if __name__ == "__main__":
    unittest.main(verbosity=2)
