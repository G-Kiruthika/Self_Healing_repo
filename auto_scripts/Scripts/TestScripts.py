# Existing content of TestScripts.py
# ... (existing test methods)

import unittest
from selenium import webdriver
from auto_scripts.Pages.LoginPage import LoginPage

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

    def test_tc_login_01_valid_login_dashboard(self):
        """
        Test Case TC_LOGIN_01:
        1. Navigate to login page
        2. Enter valid registered email address
        3. Enter valid password for the email
        4. Click on the 'Login' button
        5. Verify user is redirected to homepage/dashboard (dashboard header or user profile icon visible)
        """
        driver = webdriver.Chrome()
        page = LoginPage(driver)
        try:
            results = page.login_with_valid_credentials_tc_login_01(email='user1@example.com', password='ValidPassword123')
            self.assertTrue(results['page_opened'], 'Login page was not opened.')
            self.assertTrue(results['email_entered'], 'Email was not entered.')
            self.assertTrue(results['password_entered'], 'Password was not entered.')
            self.assertTrue(results['login_clicked'], 'Login button was not clicked.')
            self.assertTrue(results['dashboard_displayed'], 'Dashboard was not displayed.')
            self.assertTrue(results['test_passed'], 'TC_LOGIN_01 failed overall.')
        finally:
            driver.quit()

if __name__ == "__main__":
    unittest.main()
