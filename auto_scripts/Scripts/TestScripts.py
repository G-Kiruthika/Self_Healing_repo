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

    def test_tc019_login_with_special_unicode(self):
        """
        Test Case TC019:
        1. Enter valid email and password containing special characters and Unicode.
           [Test Data: üser+name@example.com / P@sswørd!🔒]
        2. Click 'Login' button.
        3. Verify that fields accept input and login succeeds if credentials are valid.
        """
        driver = webdriver.Chrome()
        page = LoginPage(driver)
        try:
            result = page.login_with_special_unicode('üser+name@example.com', 'P@sswørd!🔒')
            self.assertTrue(result, "TC019 failed: Fields did not accept special/Unicode input or login did not succeed.")
        finally:
            driver.quit()

if __name__ == "__main__":
    unittest.main()
