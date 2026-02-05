# Selenium Test Script for TC_LOGIN_001: Login functionality
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
import time

from auto_scripts.Pages.LoginPage import LoginPage

class TestLoginTCLOGIN001(unittest.TestCase):
    """
    Test Case ID: TC_LOGIN_001
    Test Description: Verify successful login with valid credentials
    """
    @classmethod
    def setUpClass(cls):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        try:
            cls.driver = webdriver.Chrome(options=options)
            cls.driver.implicitly_wait(10)
        except WebDriverException as e:
            raise Exception(f"WebDriver initialization failed: {e}")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        self.login_page = LoginPage(self.driver)

    def test_TC_LOGIN_001(self):
        """
        Steps:
        1. Navigate to the login page
        2. Enter valid registered email in the email field
        3. Enter correct password in the password field
        4. Click on the Login button
        5. Verify user session is created
        """
        # Step 1: Navigate to the login page
        login_page_displayed = self.login_page.navigate_to_login()
        self.assertTrue(login_page_displayed, "Login page should be displayed with email and password fields.")

        # Step 2: Enter valid registered email
        email = "testuser@example.com"
        email_entered = self.login_page.enter_email(email)
        self.assertTrue(email_entered, f"Email '{email}' should be accepted and displayed in the field.")

        # Step 3: Enter correct password
        password = "ValidPass123!"
        password_entered = self.login_page.enter_password(password)
        self.assertTrue(password_entered, "Password should be masked and accepted.")

        # Step 4: Click on the Login button
        dashboard_displayed = self.login_page.click_login()
        self.assertTrue(dashboard_displayed, "User should be authenticated and redirected to dashboard.")

        # Step 5: Verify user session is created
        session_verified = self.login_page.verify_user_session()
        self.assertTrue(session_verified, "User session should be created and user profile displayed.")

if __name__ == "__main__":
    unittest.main()
