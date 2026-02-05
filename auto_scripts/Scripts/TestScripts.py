import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from auto_scripts.Pages.LoginPage import LoginPage
from auto_scripts.PageClasses.UsernameRecoveryPage import UsernameRecoveryPage

class TestLoginPage(unittest.TestCase):
    # Existing test methods...
    ...
    def test_tc_login_06_empty_email_and_password_error(self): ...
    def test_tc_login_002_remember_me_checkbox_absence(self): ...
    def test_tc019_login_with_special_unicode_characters(self): ...

    def test_tc_login_003_forgot_username_recovery(self):
        """
        Test Case TC_LOGIN_003:
        1. Navigate to the login screen.
        2. Click on 'Forgot Username' link.
        3. Follow the instructions to recover username.
        4. Assert that username recovery instructions are followed and username is retrieved.
        """
        driver = webdriver.Chrome()
        try:
            login_page = LoginPage(driver)
            login_page.open_login_page()
            self.assertTrue(login_page.is_on_login_page(), "Login screen is not displayed.")
            login_page.click_forgot_username()
            recovery_page = UsernameRecoveryPage(driver)
            self.assertTrue(recovery_page.is_username_recovery_page_displayed(), "Username Recovery page is not displayed.")
            results = recovery_page.recover_username_flow_tc_login_003(email='user@example.com')
            self.assertTrue(results['clicked_forgot_username'], "Failed to click 'Forgot Username' link.")
            self.assertTrue(results['recovery_page_displayed'], "Username Recovery page not displayed after clicking link.")
            self.assertTrue(results['instructions_followed_and_email_submitted'], "Failed to follow instructions and submit email.")
            self.assertIsNotNone(results['success_message'], "No success message after username recovery.")
            self.assertIsNotNone(results['retrieved_username'], "No username retrieved after recovery.")
        finally:
            driver.quit()

    def test_tc_login_06_01_maximum_allowed_credentials(self):
        """
        Test Case TC_LOGIN_06_01:
        1. Navigate to the login page.
        2. Enter an email address with the maximum allowed length (254 characters).
        3. Enter a password with the maximum allowed length (128 characters).
        4. Click the 'Login' button.
        5. Verify that the user is successfully logged in and redirected to the dashboard.
        """
        driver = webdriver.Chrome()
        try:
            login_page = LoginPage(driver)
            login_page.login_with_maximum_allowed_credentials_and_verify_success()
        finally:
            driver.quit()

    def test_tc_login_07_02_short_email_and_password_error(self):
        """
        Test Case TC_LOGIN_07_02:
        1. Navigate to the login page.
        2. Enter an email address shorter than the minimum allowed length (e.g., 'a@').
        3. Enter a password shorter than the minimum allowed length (e.g., 'abc').
        4. Click the 'Login' button.
        5. Assert error is shown and login is not allowed.
        """
        driver = webdriver.Chrome()
        try:
            login_page = LoginPage(driver)
            result = login_page.login_with_short_email_and_password_and_validate_error(email="a@", password="abc")
            self.assertTrue(result["error_displayed"] or result["validation_displayed"], "Expected error or validation message, but none was displayed.")
            self.assertFalse(login_page.is_dashboard_displayed(), "Dashboard should not be displayed for invalid login.")
            self.assertFalse(login_page.is_user_profile_icon_displayed(), "User profile icon should not be displayed for invalid login.")
        finally:
            driver.quit()

    def test_tc_login_08_01_special_characters_success(self):
        """
        Test Case TC_LOGIN_08_01:
        1. Navigate to the login page.
        2. Enter a valid email address containing allowed special characters (e.g., dot, underscore, plus).
        3. Enter a valid password containing special characters.
        4. Click the 'Login' button.
        5. Assert successful login by checking dashboard and user profile icon visibility.
        """
        driver = webdriver.Chrome()
        try:
            login_page = LoginPage(driver)
            result = login_page.login_with_special_characters_and_validate_success(email="user.name+tag@example.com", password="P@ssw0rd!#")
            self.assertTrue(result["dashboard_displayed"], "Dashboard should be displayed for valid login.")
            self.assertTrue(result["user_profile_icon_displayed"], "User profile icon should be displayed for valid login.")
        finally:
            driver.quit()

if __name__ == "__main__":
    unittest.main()
