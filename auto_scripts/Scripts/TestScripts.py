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

    # ...other existing test methods...

    def test_tc_login_002_remember_me_checkbox_absence(self):
        """
        Test Case TC_LOGIN_002:
        1. Navigate to the login screen.
        2. Check for the presence of 'Remember Me' checkbox.
        3. Assert that 'Remember Me' checkbox is NOT present.
        """
        driver = webdriver.Chrome()
        page = LoginPage(driver)
        try:
            result = page.is_remember_me_checkbox_absent()
            self.assertTrue(result, "TC_LOGIN_002 failed: 'Remember Me' checkbox is present on login screen.")
        finally:
            driver.quit()

    def test_tc_login_06_02_excessive_email_length(self):
        """
        Test Case TC_LOGIN_06_02:
        1. Navigate to login page.
        2. Enter an email address exceeding 255 characters.
        3. Enter a valid password.
        4. Click the 'Login' button.
        5. Verify that login is not allowed and an error message or validation feedback is displayed.
        """
        driver = webdriver.Chrome()
        page = LoginPage(driver)
        try:
            long_email = 'u' * 256 + '@example.com'  # 256+ chars
            valid_password = 'ValidPassword1!'
            result = page.tc_login_06_02_excessive_email_length(long_email, valid_password)
            self.assertTrue(result['login_blocked'], "TC_LOGIN_06_02 failed: Login was not blocked for excessive email length.")
            self.assertTrue(result['validation_error'] or result['error_message'], "TC_LOGIN_06_02 failed: No error or validation message displayed.")
        finally:
            driver.quit()

if __name__ == "__main__":
    unittest.main()
