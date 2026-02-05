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

    def test_invalid_login(self, driver):
        """
        TC_LOGIN_002: Invalid Login Attempt
        Steps:
        1. Navigate to the login page
        2. Enter invalid username (invaliduser@example.com)
        3. Enter valid password (ValidPass123!)
        4. Click on the Login button
        5. Verify error message 'Invalid username or password' is displayed and user remains on login page
        """
        login_page = LoginPage(driver)
        login_page.go_to_login_page()
        assert login_page.is_loaded(), "Login page did not load successfully"
        assert login_page.enter_email("invaliduser@example.com"), "Invalid username input failed"
        assert login_page.enter_password("ValidPass123!"), "Valid password input failed"
        login_page.click_login()
        # Wait for error message and validate
        error_displayed = login_page.is_error_message_displayed()
        assert error_displayed, "Error message was not displayed after invalid login attempt"
        error_element = login_page.wait.until(
            login_page.wait._driver.find_element(*login_page.ERROR_MESSAGE)
        )
        assert "Invalid username or password" in error_element.text, f"Unexpected error message: {error_element.text}"
        # Ensure user remains on login page
        assert driver.current_url.startswith(login_page.LOGIN_URL), "User was redirected away from login page after invalid login"

    def test_login_invalid_password_tc_login_003(self, driver):
        """
        TC_LOGIN_003: Login with valid username and invalid password
        Steps:
        1. Navigate to the login page
        2. Enter valid username (testuser@example.com)
        3. Enter invalid password (WrongPassword123)
        4. Click on the Login button
        5. Verify error message 'Invalid username or password' is displayed and user remains on login page
        """
        login_page = LoginPage(driver)
        result = login_page.tc_login_003_invalid_password(
            email="testuser@example.com",
            invalid_password="WrongPassword123"
        )
        assert result, "TC_LOGIN_003 failed: Error message not displayed or user not on login page after invalid password"
