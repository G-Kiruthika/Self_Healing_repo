# Selenium Test Script for LoginPage (TC_LOGIN_002)
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Pages')))
from LoginPage import LoginPage

class TestLoginPage(unittest.TestCase):
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
            raise RuntimeError(f"WebDriver initialization failed: {e}")
        cls.login_page = LoginPage(cls.driver)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_TC_LOGIN_002_invalid_login(self):
        """
        Test Case TC_LOGIN_002
        Steps:
        1. Navigate to the login page
        2. Enter invalid email address
        3. Enter valid password
        4. Click on the Login button
        5. Assert error message is displayed
        Acceptance Criteria: SCRUM-91
        """
        invalid_email = "invaliduser@example.com"
        valid_password = "ValidPass123!"
        expected_error = "Invalid email or password"

        # Step 1: Navigate to login page
        self.login_page.go_to_login_page()
        self.assertTrue(self.login_page.is_login_fields_visible(), "Login fields not visible")

        # Step 2: Enter invalid email address
        self.assertTrue(self.login_page.enter_email(invalid_email), f"Email '{invalid_email}' not entered")

        # Step 3: Enter valid password
        self.assertTrue(self.login_page.enter_password(valid_password), "Password not entered/masked")

        # Step 4: Click Login
        self.login_page.click_login()
        time.sleep(1)  # Wait for error message to appear

        # Step 5: Assert error message is displayed
        self.assertTrue(self.login_page.is_error_message_displayed(expected_error), f"Expected error '{expected_error}' not shown")

if __name__ == "__main__":
    unittest.main()
