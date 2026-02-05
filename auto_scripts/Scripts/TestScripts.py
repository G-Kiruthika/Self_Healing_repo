# Existing content of TestScripts.py
# ... (existing test methods)

import unittest
from selenium import webdriver
from auto_scripts.Pages.LoginPage import LoginPage

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

    def test_tc019_login_with_unicode_and_special_characters(self):
        """
        Test Case TC019:
        1. Navigate to login page.
        2. Enter valid email and password containing special characters and Unicode (e.g., 'üser+name@example.com' / 'P@sswørd!🔒').
        3. Verify that the fields accept input.
        4. Submit login.
        5. Assert that login is successful (dashboard and user profile icon are displayed).
        """
        driver = webdriver.Chrome()
        page = LoginPage(driver)
        email = "üser+name@example.com"
        password = "P@sswørd!🔒"
        try:
            result = page.login_with_unicode_and_special_characters(email, password)
            self.assertTrue(result, "TC019 failed: Unicode/special character login unsuccessful or fields did not accept input.")
        finally:
            driver.quit()

if __name__ == "__main__":
    unittest.main()
