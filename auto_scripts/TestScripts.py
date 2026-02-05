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
        ...

    def test_login_invalid_password_tc_login_003(self, driver):
        ...

    def test_login_invalid_credentials_tc_login_004(self, driver):
        """
        TC_LOGIN_004: Verify error message for invalid login credentials.
        Steps:
        1. Navigate to login page
        2. Enter invalid username 'wronguser@example.com'
        3. Enter invalid password 'WrongPass456'
        4. Click login
        5. Assert error message 'Invalid username or password' is displayed
        """
        login_page = LoginPage(driver)
        login_page.load()
        assert login_page.is_displayed(), "Login page did not load properly."

        login_page.enter_email('wronguser@example.com')
        login_page.enter_password('WrongPass456')
        login_page.click_login()

        # Wait for error message to be visible and retrieve it
        error_message = login_page.get_error_message()
        assert error_message is not None, "No error message was displayed after invalid login."
        assert error_message.strip() == 'Invalid username or password', (
            f"Expected error message 'Invalid username or password', but got '{error_message.strip()}'"
        )
