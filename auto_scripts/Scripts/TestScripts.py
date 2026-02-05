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

    def test_tc_login_003_invalid_password(self, driver):
        """
        Test Case TC_LOGIN_003:
        1. Navigate to the login page.
        2. Enter valid email and incorrect password (email: user@example.com, password: WrongPass456).
        3. Click the 'Login' button.
        4. Error message for incorrect password is shown.
        5. Login is not successful.
        """
        login_page = LoginPage(driver)
        login_page.open_login_page()
        login_page.login_with_credentials('user@example.com', 'WrongPass456')
        error_message = login_page.get_incorrect_password_error_message()
        assert error_message is not None and error_message != "", "Error message not displayed for incorrect password."
        assert login_page.is_login_unsuccessful(), "Login should not succeed with incorrect password."
