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

    def test_tc017_invalid_login_error_accessibility(self):
        """
        Test Case TC017:
        1. Trigger error message by invalid login (user@example.com / WrongPassword).
        2. Verify error message is displayed in clear text and accessible to screen readers (ARIA attributes).
        """
        driver = webdriver.Chrome()
        page = LoginPage(driver)
        try:
            result = page.tc017_invalid_login_error_accessibility('user@example.com', 'WrongPassword')
            self.assertTrue(result, "TC017 failed: Error message not displayed in clear text or not accessible to screen readers.")
        finally:
            driver.quit()

if __name__ == "__main__":
    unittest.main()
