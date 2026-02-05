# Existing content of TestScripts.py
# ... (existing test methods)

import unittest
from selenium import webdriver
from auto_scripts.Pages.LoginPage import LoginPage
from auto_scripts.Pages.PasswordRecoveryPage import PasswordRecoveryPage

class TestLoginPage(unittest.TestCase):
    # Existing test methods...

    def test_tc_login_017_verify_password_field_masking(self):
        """
        Test Case TC_LOGIN_017:
        1. Navigate to login page and verify display.
        2. Enter password 'ValidPass123' and verify masking.
        """
        driver = webdriver.Chrome()
        page = LoginPage(driver)
        try:
            result = page.tc_login_017_verify_password_field_masking('ValidPass123')
            self.assertTrue(result, "TC_LOGIN_017 failed: Password field masking not verified.")
        finally:
            driver.quit()

    def test_tc_login_012_password_recovery_flow(self):
        """
        Test Case TC_LOGIN_012 (Password Recovery):
        1. Navigate to login page.
        2. Click on 'Forgot Password' link.
        3. Enter registered email and submit (use 'user@example.com').
        4. Assert password reset email is sent.
        """
        driver = webdriver.Chrome()
        page = PasswordRecoveryPage(driver)
        try:
            result = page.tc_login_012_password_recovery_flow('user@example.com')
            self.assertTrue(result, "TC_LOGIN_012 failed: Password recovery flow did not complete successfully.")
        finally:
            driver.quit()

if __name__ == "__main__":
    unittest.main()
