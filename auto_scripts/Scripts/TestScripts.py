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

    def test_tc_login_004(self, driver):
        """
        Test Case TC_LOGIN_004:
        1. Navigate to the login page.
        2. Leave email and password fields empty.
        3. Click the 'Login' button.
        4. Verify error messages for required fields are shown.
        5. Verify login is not successful.
        """
        login_page = LoginPage(driver)
        login_page.open_login_page()
        result = login_page.validate_required_field_errors_tc_login_004()
        assert result["empty_prompt"] is not None, "Mandatory fields prompt should be displayed."
        assert result["login_unsuccessful"], "Login should not be successful when required fields are empty."
        assert (result["error_message"] is not None or result["validation_error"] is not None), "Error or validation message should be shown for empty fields."
