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
        4. Assert that username recovery instructions are followed and confirmation or error is retrieved.
        """
        driver = webdriver.Chrome()
        try:
            login_page = LoginPage(driver)
            login_page.open_login_page()
            self.assertTrue(login_page.is_on_login_page(), "Login screen is not displayed.")
            clicked = login_page.click_forgot_username()
            self.assertTrue(clicked, "Could not click 'Forgot Username' link.")
            recovery_page = UsernameRecoveryPage(driver)
            recovery_page.go_to_username_recovery()
            recovery_page.enter_email('user@example.com')
            recovery_page.submit_recovery()
            confirmation = recovery_page.get_confirmation_message()
            error = recovery_page.get_error_message()
            self.assertTrue(confirmation or error, "No confirmation or error message received after username recovery.")
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

    def test_tc_login_07_02_too_short_credentials_error(self):
        """
        Test Case TC_LOGIN_07_02:
        1. Navigate to the login page.
        2. Enter an email address shorter than the minimum allowed length (e.g., 'a@').
        3. Enter a password shorter than the minimum allowed length (e.g., 'abc').
        4. Click the 'Login' button.
        5. Assert that login is not allowed and the appropriate error message is shown.
        """
        driver = webdriver.Chrome()
        try:
            login_page = LoginPage(driver)
            login_page.login_with_too_short_credentials_and_validate_error(
                email="a@",
                password="abc",
                expected_error="Mandatory fields are required"
            )
        finally:
            driver.quit()

if __name__ == "__main__":
    unittest.main()