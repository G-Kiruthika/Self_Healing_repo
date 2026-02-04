# Selenium Test Script for TC_LOGIN_016: Account Lockout Scenario
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
import time
import os
import sys

# Add Pages directory to sys.path for import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../Pages')))
from LoginPage import LoginPage

def get_chrome_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(options=options)

@pytest.mark.login
@pytest.mark.account_lockout
class TestLoginAccountLockout:
    """
    Test Case TC_LOGIN_016: Account lockout after 5 failed login attempts.
    Acceptance Criteria: SCRUM-91
    """
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        self.driver = get_chrome_driver()
        self.driver.implicitly_wait(5)
        self.login_page = LoginPage(self.driver)
        yield
        self.driver.quit()

    def test_account_lockout_after_failed_attempts(self):
        """
        Steps:
        1. Navigate to the login page
        2. Enter valid email and incorrect password, click Login (Attempt 1)
        3. Repeat login with incorrect password (Attempts 2-4)
        4. Attempt login with incorrect password for the 5th time
        5. Attempt login with correct password
        Expected:
        - Error message after each failed attempt
        - After 5th attempt, account is locked, lockout message is displayed
        - Login is blocked even with correct password, lockout message persists
        """
        # Test Data
        email = "testuser@example.com"
        wrong_passwords = [
            "WrongPass1",
            "WrongPass2",
            "WrongPass3",
            "WrongPass4",
            "WrongPass5"
        ]
        correct_password = "ValidPass123!"
        expected_lockout = "Account has been locked due to multiple failed login attempts. Please try again after 30 minutes or reset your password"

        # Step 1: Navigate to login page
        self.login_page.go_to_login_page()
        assert self.login_page.is_login_fields_visible(), "Login page is not displayed."

        # Step 2: Attempt 1 - invalid password
        assert self.login_page.enter_email(email), "Email was not entered correctly on attempt 1!"
        assert self.login_page.enter_password(wrong_passwords[0]), "Password was not entered/masked correctly on attempt 1!"
        self.login_page.click_login()
        time.sleep(1)
        error_message = self.login_page.get_error_message()
        assert error_message is not None, "No error message displayed after 1st failed attempt!"
        assert "error" in error_message.lower(), f"Unexpected error message after 1st failed attempt: {error_message}"
        assert self.driver.current_url == self.login_page.LOGIN_URL, "User should remain on login page after failed attempt!"

        # Step 3: Attempts 2-4
        for i in range(1, 4):
            assert self.login_page.enter_email(email), f"Email was not entered correctly on attempt {i+1}!"
            assert self.login_page.enter_password(wrong_passwords[i]), f"Password was not entered/masked correctly on attempt {i+1}!"
            self.login_page.click_login()
            time.sleep(1)
            error_message = self.login_page.get_error_message()
            assert error_message is not None, f"No error message displayed after {i+1} failed attempt!"
            assert "error" in error_message.lower(), f"Unexpected error message after {i+1} failed attempt: {error_message}"
            assert self.driver.current_url == self.login_page.LOGIN_URL, "User should remain on login page after failed attempt!"

        # Step 4: 5th attempt - lockout
        assert self.login_page.enter_email(email), "Email was not entered correctly on 5th attempt!"
        assert self.login_page.enter_password(wrong_passwords[4]), "Password was not entered/masked correctly on 5th attempt!"
        self.login_page.click_login()
        time.sleep(1)
        error_message = self.login_page.get_error_message()
        assert error_message is not None, "No error message displayed after 5th failed attempt!"
        assert expected_lockout.lower() in error_message.lower(), f"Expected lockout message not found: {error_message}"
        assert self.driver.current_url == self.login_page.LOGIN_URL, "User should remain on login page after lockout!"

        # Step 5: Attempt login with correct password (should still be locked)
        assert self.login_page.enter_email(email), "Email was not entered correctly after lockout!"
        assert self.login_page.enter_password(correct_password), "Password was not entered/masked correctly after lockout!"
        self.login_page.click_login()
        time.sleep(1)
        error_message = self.login_page.get_error_message()
        assert error_message is not None, "No error message displayed after login attempt during lockout!"
        assert expected_lockout.lower() in error_message.lower(), f"Lockout message not displayed after login attempt with correct password: {error_message}"
        assert self.driver.current_url == self.login_page.LOGIN_URL, "User should remain on login page during lockout!"
