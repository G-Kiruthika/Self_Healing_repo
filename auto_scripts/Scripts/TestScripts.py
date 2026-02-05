import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from auto_scripts.Pages.LoginPage import LoginPage
from auto_scripts.Pages.PasswordRecoveryPage import PasswordRecoveryPage
from auto_scripts.Pages.UsernameRecoveryPage import UsernameRecoveryPage

class TestLoginPage(unittest.TestCase):
    # Existing test methods...
    ...
    def test_tc_login_06_empty_email_and_password_error(self):
        ...
    def test_tc_login_002_remember_me_checkbox_absence(self):
        ...
    def test_tc_login_06_02_excessive_email_length(self):
        ...

    def test_tc_login_003_forgot_username_workflow(self):
        """
        Test Case TC_LOGIN_003:
        1. Navigate to login screen.
        2. Click on 'Forgot Username' link.
        3. Follow instructions to recover username.
        4. Validate username recovery success.
        """
        driver = webdriver.Chrome()
        try:
            login_page = LoginPage(driver)
            login_page.go_to_login_page()
            login_page.click_forgot_username()
            recovery_page = UsernameRecoveryPage(driver)
            test_email = "user@example.com"
            confirmation = recovery_page.recover_username(test_email)
            self.assertIsNotNone(confirmation, "Username recovery failed or no confirmation message displayed.")
            self.assertTrue("success" in confirmation.lower() or "retrieved" in confirmation.lower(), f"Unexpected confirmation message: {confirmation}")
        finally:
            driver.quit()

if __name__ == "__main__":
    unittest.main()
