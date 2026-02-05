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

if __name__ == "__main__":
    unittest.main()
