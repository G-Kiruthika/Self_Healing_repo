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
        """
        Test Case TC_LOGIN_002:
        1. Navigate to the login page.
        2. Enter invalid email format and valid password.
        3. Click the 'Login' button.
        4. Verify error message for invalid email format is shown.
        5. Ensure login is not successful.
        """
        login_page = LoginPage(driver)
        result = login_page.tc_login_002_invalid_email_login('userexample.com', 'ValidPass123')
        assert result is True
