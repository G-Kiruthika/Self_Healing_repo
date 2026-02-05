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

if __name__ == "__main__":
    unittest.main()
