# Selenium Test Script for TC_SCRUM74_007: Validation errors for empty email/username and password fields
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import sys
import os

# Ensure Pages directory is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../Pages')))
from LoginPage import LoginPage

class TestTCSCRUM74_007_EmptyFieldsLoginValidation(unittest.TestCase):
    """
    Test Case ID: TC_SCRUM74_007
    Title: Validation errors for empty email/username and password fields
    Steps:
        1. Navigate to the login page
        2. Leave email/username field empty
        3. Leave password field empty
        4. Click on the Login button
        5. Validation errors displayed for both fields: 'Email/Username and Password are required'
    """

    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(10)
        cls.login_page = LoginPage(cls.driver)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_empty_fields_login_validation(self):
        # Step 1: Navigate to the login page
        login_page_displayed = self.login_page.navigate_to_login()
        self.assertTrue(login_page_displayed, "Login page should be displayed.")

        # Step 2: Leave email/username field empty
        email_empty = self.login_page.leave_email_field_empty()
        self.assertTrue(email_empty, "Email/username field should be empty.")

        # Step 3: Leave password field empty
        password_empty = False
        try:
            password_field = self.login_page.driver.find_element(*self.login_page.PASSWORD_INPUT)
            password_field.clear()
            password_empty = password_field.get_attribute("value") == ""
        except NoSuchElementException:
            password_empty = False
        self.assertTrue(password_empty, "Password field should be empty.")

        # Step 4: Click on the Login button
        self.login_page.driver.find_element(*self.login_page.LOGIN_BUTTON).click()
        time.sleep(1)  # Wait for validation errors to appear

        # Step 5: Validation errors displayed for both fields
        email_error = self.login_page.is_validation_error_displayed("Email/Username is required")
        password_error = self.login_page.is_validation_error_displayed("Password is required")
        self.assertTrue(email_error, "Validation error for email/username should be displayed.")
        self.assertTrue(password_error, "Validation error for password should be displayed.")

        # Final assertion: Both errors must be present
        self.assertTrue(email_error and password_error, "Both validation errors must be displayed.")

if __name__ == "__main__":
    unittest.main()
