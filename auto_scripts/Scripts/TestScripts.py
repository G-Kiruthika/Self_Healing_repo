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

    # ...other existing test methods...

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

    def test_tc_login_003_forgot_username_workflow(self):
        """
        Test Case TC_LOGIN_003:
        1. Navigate to the login screen.
        2. Click on 'Forgot Username' link.
        3. Follow the instructions to recover username.
        4. Validate username is retrieved.
        """
        driver = webdriver.Chrome()
        login_page = LoginPage(driver)
        username_recovery_page = UsernameRecoveryPage(driver)
        try:
            # Step 1: Navigate to login page
            login_page.go_to_login_page()
            self.assertTrue(login_page.is_on_login_page(), "Login page not displayed.")

            # Step 2: Click 'Forgot Username' link
            login_page.click_forgot_username()

            # Step 3: Validate instructions are displayed
            self.assertTrue(username_recovery_page.is_instructions_displayed(), "Username recovery instructions not displayed.")

            # Step 4: Enter recovery email (example email used)
            recovery_email = "testuser@example.com"
            username_recovery_page.enter_recovery_email(recovery_email)

            # Step 5: Submit recovery
            username_recovery_page.submit_recovery()

            # Step 6: Validate success message and username retrieval
            success_msg = username_recovery_page.get_success_message()
            self.assertIsNotNone(success_msg, "Success message not displayed after username recovery.")
            recovered_username = username_recovery_page.get_recovered_username()
            self.assertIsNotNone(recovered_username, "Recovered username not displayed.")
        finally:
            driver.quit()

if __name__ == "__main__":
    unittest.main()
