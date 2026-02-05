# Selenium Test Script for TC_SCRUM-74_001
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
import time
import os
import sys

# Ensure the Pages module is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../Pages')))
from LoginPage import LoginPage

class TestLoginTCSCRUM74001(unittest.TestCase):
    """
    Test Case: TC_SCRUM-74_001
    Title: End-to-end login and session validation
    Steps:
        1. Navigate to the login page
        2. Enter valid registered username in the username field
        3. Enter valid password in the password field
        4. Click on the Login button
        5. Verify user session is created and user profile is displayed
    Acceptance Criteria:
        - Login page is displayed with username and password fields
        - Username is entered successfully in the field
        - Password is masked and entered successfully
        - User is authenticated and redirected to the dashboard/home page
        - User is successfully logged in, session token is generated, and user name is displayed in the header
    """

    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        try:
            cls.driver = webdriver.Chrome(options=chrome_options)
            cls.driver.implicitly_wait(10)
        except WebDriverException as e:
            raise RuntimeError(f"WebDriver could not be initialized: {e}")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        self.login_page = LoginPage(self.driver)

    def test_TC_SCRUM_74_001_login_success(self):
        """
        Automates TC_SCRUM-74_001: End-to-end login and session validation.
        """
        # Test Data
        username = "testuser@example.com"
        password = "ValidPass123!"

        # Step 1: Navigate to the login page
        self.login_page.go_to_login_page()
        self.assertTrue(self.login_page.is_login_fields_visible(), "Login fields are not visible!")
        self.assertIn("login", self.driver.current_url, "Not on login page URL!")

        # Step 2: Enter valid registered username
        self.assertTrue(self.login_page.enter_email(username), "Username was not entered successfully!")
        email_field = self.driver.find_element(*LoginPage.EMAIL_FIELD)
        self.assertEqual(email_field.get_attribute("value"), username, "Username value mismatch in field!")

        # Step 3: Enter valid password
        self.assertTrue(self.login_page.enter_password(password), "Password was not entered/masked successfully!")
        password_field = self.driver.find_element(*LoginPage.PASSWORD_FIELD)
        self.assertEqual(password_field.get_attribute("type"), "password", "Password field is not masked!")

        # Step 4: Click on the Login button
        self.login_page.click_login()
        time.sleep(2)  # Wait for page navigation

        # Step 5: Verify user session is created and user profile is displayed
        self.assertTrue(self.login_page.is_redirected_to_dashboard(), "User was not redirected to dashboard/home page!")
        self.assertTrue(self.login_page.is_session_token_created(), "User session token not generated or user name not displayed in header!")

    def tearDown(self):
        # Optional: log out if needed, or clear cookies
        self.driver.delete_all_cookies()

if __name__ == "__main__":
    unittest.main()
