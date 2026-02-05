import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from auto_scripts.Pages.LoginPage import LoginPage
from auto_scripts.Pages.PasswordRecoveryPage import PasswordRecoveryPage

class TestLoginPage(unittest.TestCase):
    # Existing test methods...
    # ...
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

    def test_tc_login_01_end_to_end_login_and_dashboard_verification(self):
        """
        Test Case TC_LOGIN_01:
        1. Navigate to login page
        2. Enter valid email ('user1@example.com')
        3. Enter valid password ('ValidPassword123')
        4. Click login
        5. Verify dashboard is displayed
        """
        driver = webdriver.Chrome()
        page = LoginPage(driver)
        try:
            results = page.login_and_validate_dashboard_tc_login_01(email="user1@example.com", password="ValidPassword123")
            self.assertTrue(results.get('login_page_opened'), "Login page did not open.")
            self.assertTrue(results.get('email_entered'), "Email was not entered.")
            self.assertTrue(results.get('password_entered'), "Password was not entered.")
            self.assertTrue(results.get('login_clicked'), "Login button was not clicked.")
            self.assertTrue(results.get('dashboard_displayed'), "Dashboard was not displayed after login.")
        finally:
            driver.quit()

if __name__ == "__main__":
    unittest.main()
