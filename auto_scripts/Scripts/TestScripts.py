# Import necessary modules
from auto_scripts.Pages.LoginPage import LoginPage
from auto_scripts.Pages.ForgotPasswordPage import ForgotPasswordPage
from auto_scripts.Pages.UsernameRecoveryPage import UsernameRecoveryPage
from auto_scripts.Pages.PasswordRecoveryPage import PasswordRecoveryPage
from auto_scripts.Pages.ResetPasswordPage import ResetPasswordPage
from selenium.webdriver.common.by import By
import pytest

class TestLogin:
    
    def test_TC_LOGIN_002_invalid_email_format(self, driver):
        '''
        TC_LOGIN_002: Attempts login with invalid email format and valid password, expects validation error message.
        Steps:
            1. Navigate to the login page.
            2. Enter invalid email format ('userexample.com') and valid password ('ValidPass123').
            3. Click the 'Login' button.
        Expected:
            Error message for invalid email format is shown. Login is not successful.
        '''
        login_page = LoginPage(driver)
        result = login_page.login_with_invalid_email_format('userexample.com', 'ValidPass123')
        assert result, "Validation error for invalid email format should be displayed."
