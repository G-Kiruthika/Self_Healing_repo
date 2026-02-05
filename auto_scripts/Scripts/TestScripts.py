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
        2. Ensure both username and password fields are empty
        3. Click the login button
        4. Assert that both 'Username is required' and 'Password is required' validation errors are displayed
        """
        login_page = LoginPage(driver)
        validation_errors = login_page.test_empty_fields_validation()
        assert 'Username is required' in validation_errors, "Expected 'Username is required' validation error not found."
        assert 'Password is required' in validation_errors, "Expected 'Password is required' validation error not found."

    def test_remember_me_session_persistence_tc_login_008(self, driver_factory):
        """
        TC_LOGIN_008: Remember Me Session Persistence
        Steps:
        1. Navigate to the login page (URL: https://ecommerce.example.com/login)
        2. Enter valid username and password (Username: testuser@example.com, Password: ValidPass123!)
        3. Check the Remember Me checkbox
        4. Click on the Login button
        5. Close the browser and reopen, navigate to the website
        6. Verify user session is persisted and user remains logged in
        """
        login_page = LoginPage(driver_factory())
        result = login_page.test_remember_me_session_persistence(driver_factory)
        assert result, "TC_LOGIN_008 failed: Session was not persisted after browser restart or dashboard/user icon not displayed."

    def test_remember_me_session_not_persisted_tc_login_009(self, driver_factory):
        """
        TC_LOGIN_009: Remember Me Unchecked, Session Not Persisted
        Steps:
        1. Navigate to the login page (URL: https://ecommerce.example.com/login)
        2. Enter valid username and password (Username: testuser@example.com, Password: ValidPass123!)
        3. Ensure Remember Me checkbox is unchecked
        4. Click on the Login button and close browser
        5. Reopen browser and navigate to the website
        6. Verify user is redirected to login page (session not persisted)
        """
        # Step 1: Open browser and navigate to login page
        driver1 = driver_factory()
        login_page1 = LoginPage(driver1)
        login_page1.load()
        assert login_page1.is_displayed(), "Login page is not displayed"
        # Step 2: Enter valid username and password
        login_page1.enter_email("testuser@example.com")
        login_page1.enter_password("ValidPass123!")
        # Step 3: Ensure Remember Me checkbox is unchecked
        login_page1.set_remember_me(False)
        # Step 4: Click login
        login_page1.click_login()
        # Wait for dashboard to load
        assert login_page1.is_dashboard_displayed(), "Dashboard not displayed after login"
        # Step 4b: Close browser
        driver1.quit()
        # Step 5: Reopen browser and navigate to the website
        driver2 = driver_factory()
        login_page2 = LoginPage(driver2)
        login_page2.load()
        # Step 6: Verify user is redirected to login page (session not persisted)
        is_dashboard = False
        try:
            is_dashboard = login_page2.is_dashboard_displayed()
        except Exception:
            is_dashboard = False
        is_login = False
        try:
            is_login = login_page2.is_displayed()
        except Exception:
            is_login = False
        driver2.quit()
        assert is_login and not is_dashboard, "Session persisted or login page not displayed after browser restart with Remember Me unchecked"
