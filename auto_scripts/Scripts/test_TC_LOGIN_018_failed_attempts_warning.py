# Selenium Test Script for TC_LOGIN_018 - Failed Attempts Warning Counter
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import sys
import os

# Ensure Pages directory is in sys.path for import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../Pages')))
from LoginPage import LoginPage

class TestLoginFailedAttemptsWarningCounter(unittest.TestCase):
    """
    Test Case TC_LOGIN_018: Verify warning messages for consecutive failed login attempts.
    Steps:
        1. Navigate to the login page
        2. Enter valid email and incorrect password, then click Login (Attempts 1-2)
           - Expected: Standard error message displayed
        3. Attempt login with incorrect password for the 3rd time
           - Expected: Error message with warning 'Invalid credentials. You have 2 more attempts before your account is locked' is displayed
        4. Attempt login with incorrect password for the 4th time
           - Expected: Error message with warning 'Invalid credentials. You have 1 more attempt before your account is locked' is displayed
    Acceptance Criteria: SCRUM-91
    """

    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(10)
        cls.login_page = LoginPage(cls.driver)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_failed_attempts_warning_counter(self):
        # Test Data
        email = 'testuser@example.com'
        wrong_passwords = ['WrongPass1', 'WrongPass2', 'WrongPass3', 'WrongPass4']
        # Step 1: Navigate to login page
        self.login_page.go_to_login_page()
        self.assertTrue(self.login_page.is_login_fields_visible(), "Login fields are not visible!")
        # Step 2-4: Perform 4 failed login attempts, check error/warning messages
        for idx, wrong_password in enumerate(wrong_passwords, 1):
            # Enter email and wrong password
            self.assertTrue(self.login_page.enter_email(email), f"Email was not entered correctly for attempt {idx}!")
            self.assertTrue(self.login_page.enter_password(wrong_password), f"Wrong password was not entered correctly for attempt {idx}!")
            self.login_page.click_login()
            time.sleep(1)  # Wait for error/warning message
            error_message = self.login_page.get_error_message()
            self.assertIsNotNone(error_message, f"No error message displayed for attempt {idx}!")
            error_message_lower = error_message.lower()
            if idx in [1, 2]:
                # Standard error message
                self.assertTrue(
                    "invalid credentials" in error_message_lower or "invalid email or password" in error_message_lower,
                    f"Unexpected error message on attempt {idx}: {error_message}"
                )
            elif idx == 3:
                # Warning for 2 more attempts
                expected_warning = "invalid credentials. you have 2 more attempts before your account is locked"
                self.assertIn(
                    expected_warning, error_message_lower,
                    f"Expected warning not found on attempt 3: {error_message}"
                )
            elif idx == 4:
                # Warning for 1 more attempt
                expected_warning = "invalid credentials. you have 1 more attempt before your account is locked"
                self.assertIn(
                    expected_warning, error_message_lower,
                    f"Expected warning not found on attempt 4: {error_message}"
                )
            self.assertEqual(
                self.login_page.driver.current_url, self.login_page.LOGIN_URL,
                f"User is not on login page after failed attempt {idx}!"
            )

if __name__ == '__main__':
    unittest.main()
