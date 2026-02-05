# Import necessary modules
from auto_scripts.Pages.LoginPage import LoginPage
from auto_scripts.Pages.ForgotPasswordPage import ForgotPasswordPage
from auto_scripts.Pages.UsernameRecoveryPage import UsernameRecoveryPage
from auto_scripts.Pages.PasswordRecoveryPage import PasswordRecoveryPage
from auto_scripts.Pages.ResetPasswordPage import ResetPasswordPage
from selenium.webdriver.common.by import By
import pytest

class TestLogin:
    def test_tc_login_001_login_flow(self, driver):
        login_page = LoginPage(driver)
        result = login_page.tc_login_001_login_flow('user@example.com', 'ValidPass123')
        assert result is True

    def test_tc_login_003_invalid_password_flow(self, driver):
        login_page = LoginPage(driver)
        result = login_page.tc_login_003_invalid_password_flow('user@example.com', 'WrongPass456')
        assert result is True

    def test_tc_login_002_invalid_email_login(self, driver):
        login_page = LoginPage(driver)
        result = login_page.tc_login_002_invalid_email_login('userexample.com', 'ValidPass123')
        assert result is True

    def test_tc_login_004_required_fields_validation(self, driver):
        login_page = LoginPage(driver)
        result = login_page.tc_login_004_required_fields_validation()
        assert result is True

    def test_tc_login_003(self, driver):
        """
        Test Case TC_LOGIN_003:
        1. Navigate to the login page.
        2. Enter valid email and incorrect password ('user@example.com', 'WrongPass456').
        3. Click the 'Login' button.
        4. Verify error message for incorrect password is shown.
        5. Verify login is not successful.
        """
        login_page = LoginPage(driver)
        login_page.open_login_page()
        login_page.login_with_credentials('user@example.com', 'WrongPass456')
        error_message = login_page.get_authentication_error()
        assert error_message is not None and error_message != "", "Authentication error message should be displayed for incorrect password."
        assert login_page.is_login_unsuccessful(), "Login should not be successful with incorrect password."

    def test_tc_login_005_empty_email_login(self, driver):
        """
        Test Case TC_LOGIN_005:
        1. Navigate to the login page.
        2. Leave email/username field empty and enter valid password ('', 'ValidPass123').
        3. Click the 'Login' button.
        4. Validate error message for required email/username is shown.
        5. Assert login is not successful.
        """
        login_page = LoginPage(driver)
        try:
            login_page.tc_login_005_empty_email_login('ValidPass123')
        except AssertionError as e:
            pytest.fail(str(e))
