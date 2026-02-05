# Import necessary modules
from auto_scripts.Pages.LoginPage import LoginPage
from auto_scripts.Pages.ForgotPasswordPage import ForgotPasswordPage
from auto_scripts.Pages.UsernameRecoveryPage import UsernameRecoveryPage
from selenium.webdriver.common.by import By
import pytest

class TestLogin:
    def test_valid_login(self, driver):
        # Existing test logic...
        pass

    def test_invalid_login_tc_scrum_115_002(self, driver):
        """
        TC-SCRUM-115-002: Invalid login attempt
        Steps:
        1. Navigate to the e-commerce website login page
        2. Enter invalid/non-existent username in the username field
        3. Enter valid password in the password field
        4. Click on the Login button
        5. Verify user remains on login page and error message is displayed
        """
        # Step 1: Navigate to login page
        login_page = LoginPage(driver)
        # Step 2 & 3 & 4: Attempt invalid login with provided test data
        result = login_page.attempt_invalid_login(
            invalid_email='invaliduser@example.com',
            valid_password='ValidPass123!'
        )
        # Step 5: Verify error message and user remains on login page
        assert result, "Error message not displayed or user not on login page after invalid login attempt."
