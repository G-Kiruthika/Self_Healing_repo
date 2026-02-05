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

    def test_login_empty_username_tc_login_005(self, driver):
        """
        TC_LOGIN_005: Login with empty username and valid password
        Steps:
        1. Navigate to the login page
        2. Leave username field empty
        3. Enter valid password ('ValidPass123!')
        4. Click on the Login button
        5. Verify validation error 'Username is required' is displayed
        """
        login_page = LoginPage(driver)
        error_message = login_page.login_with_empty_username('ValidPass123!')
        assert 'Username is required' in error_message, f"Expected validation error not found. Got: {error_message}"

    def test_login_empty_password_tc_login_006(self, driver):
        """
        TC_LOGIN_006: Login with valid username and empty password
        Steps:
        1. Navigate to the login page
        2. Enter valid username (testuser@example.com)
        3. Leave password field empty
        4. Click on the Login button
        5. Verify validation error 'Password is required' is displayed
        """
        login_page = LoginPage(driver)
        result = login_page.test_login_empty_password_validation()
        assert result, "TC_LOGIN_006 failed: Validation error not displayed or incorrect after empty password submission"

    def test_login_empty_fields_tc_login_007(self, driver):
        """
        TC_LOGIN_007: Login with both username and password fields empty
        Steps:
        1. Navigate to the login page
        2. Leave both username and password fields empty
        3. Click on the Login button
        4. Verify validation errors 'Username is required' and 'Password is required' are displayed
        """
        login_page = LoginPage(driver)
        login_page.load()
        assert login_page.is_displayed(), "Login page is not displayed"
        # Clear both fields to ensure they are empty
        email_elem = login_page.wait.until(lambda d: d.find_element(*login_page.EMAIL_FIELD))
        email_elem.clear()
        password_elem = login_page.wait.until(lambda d: d.find_element(*login_page.PASSWORD_FIELD))
        password_elem.clear()
        login_page.click_login()
        # Check for both validation errors
        validation_errors = driver.find_elements(By.CSS_SELECTOR, ".invalid-feedback")
        errors_text = [e.text for e in validation_errors if e.is_displayed()]
        assert any("Username is required" in t for t in errors_text), "Validation error 'Username is required' not found."
        assert any("Password is required" in t for t in errors_text), "Validation error 'Password is required' not found."
