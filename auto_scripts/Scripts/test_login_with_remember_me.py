# Selenium Test Script for TC_LOGIN_002: Login with Remember Me
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import sys
import os

# Adjust the path to import the LoginPage
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Pages')))
from LoginPage import LoginPage

class TestLoginWithRememberMe(unittest.TestCase):
    """
    Test Case: TC_LOGIN_002
    Description: End-to-end login workflow with Remember Me checkbox.
    Steps:
        1. Navigate to the login page
        2. Enter valid username
        3. Enter valid password
        4. Check Remember Me checkbox
        5. Click Login button
        6. Verify user session is created, user is redirected to dashboard, and session is persisted
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

    def test_login_with_remember_me(self):
        email = "testuser@example.com"
        password = "Test@1234"
        # Step 1: Navigate to the login page
        self.login_page.go_to_login_page()
        self.assertTrue(self.login_page.is_login_fields_visible(), "Login fields are not visible!")

        # Step 2: Enter valid username
        self.assertTrue(self.login_page.enter_email(email), "Username was not entered correctly!")

        # Step 3: Enter valid password
        self.assertTrue(self.login_page.enter_password(password), "Password was not entered/masked correctly!")

        # Step 4: Check Remember Me checkbox
        self.assertTrue(self.login_page.check_remember_me(), "Remember Me checkbox was not selected!")

        # Step 5: Click Login button
        self.login_page.click_login()

        # Step 6: Verify user session is created, user is redirected to dashboard, and session is persisted
        self.assertTrue(self.login_page.is_redirected_to_dashboard(), "User was not redirected to dashboard!")
        self.assertTrue(self.login_page.is_session_token_created(), "User session was not created!")
        # Additional validation for session persistence can be added here

if __name__ == "__main__":
    unittest.main()
