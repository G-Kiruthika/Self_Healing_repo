# Existing content of TestScripts.py
# ... (existing test methods)

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from auto_scripts.Pages.LoginPage import LoginPage
from auto_scripts.Pages.PasswordRecoveryPage import PasswordRecoveryPage

class TestLoginPage(unittest.TestCase):
    # Existing test methods...
    ...
    def test_tc_login_06_empty_email_and_password_error(self):
        """
        Test Case TC_LOGIN_06:
        1. Navigate to login page.
        2. Leave both email and password fields empty.
        3. Click 'Login' button.
        4. Verify error messages 'Email is required' and 'Password is required' are displayed. User remains on login page.
        """
        driver = webdriver.Chrome()
        page = LoginPage(driver)
        try:
            result = page.tc_login_06_empty_email_and_password_error()
            self.assertTrue(result, "TC_LOGIN_06 failed: Expected error messages not displayed or user not on login page.")
        finally:
            driver.quit()

    # ... (other methods)

    def test_tc_login_06_02_overlong_email_error(self):
        """
        Test Case TC_LOGIN_06_02:
        1. Navigate to the login page.
        2. Enter an email address exceeding the maximum allowed length (255+ characters).
        3. Enter a valid password ('ValidPassword1!').
        4. Click the 'Login' button.
        5. Assert that an error for overlong email is displayed and login is not allowed.
        """
        driver = webdriver.Chrome()
        page = LoginPage(driver)
        try:
            result = page.login_with_overlong_email('ValidPassword1!')
            self.assertTrue(result, "TC_LOGIN_06_02 failed: Error for overlong email not displayed or login was allowed.")
        finally:
            driver.quit()

if __name__ == "__main__":
    unittest.main()
