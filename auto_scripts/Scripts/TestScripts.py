import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from auto_scripts.Pages.LoginPage import LoginPage
from auto_scripts.Pages.PasswordRecoveryPage import PasswordRecoveryPage

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

    def test_tc019_login_with_special_unicode_characters(self):
        """
        Test Case TC019:
        1. Navigate to login page.
        2. Enter valid email and password containing special characters and Unicode.
        3. Submit the login form.
        4. Assert that the dashboard is displayed to confirm successful login.
        Acceptance Criteria:
            - Fields accept special characters and Unicode input.
            - Login succeeds if credentials are valid.
        """
        driver = webdriver.Chrome()
        page = LoginPage(driver)
        try:
            # The method will raise if dashboard is not displayed, so if no exception, test passes
            page.login_with_special_unicode_characters()
            # Optionally, verify dashboard header is present (redundant, as method already waits for it)
            dashboard_header = (By.CSS_SELECTOR, "h1.dashboard-title")
            dashboard_present = driver.find_element(*dashboard_header).is_displayed()
            self.assertTrue(dashboard_present, "TC019 failed: Dashboard not displayed after login with special Unicode characters.")
        finally:
            driver.quit()

    def test_tc_login_001_invalid_login_error_message(self):
        """
        Test Case TC_LOGIN_001:
        1. Navigate to the login screen.
        2. Validate login screen is displayed.
        3. Enter invalid username and/or password.
        4. Validate error message 'Invalid username or password. Please try again.' is displayed and user stays on login page.
        """
        driver = webdriver.Chrome()
        page = LoginPage(driver)
        try:
            email = "invalid@example.com"
            invalid_password = "wrongpassword"
            expected_error = "Invalid username or password. Please try again."
            page.perform_invalid_login_and_validate(email, invalid_password, expected_error)
        finally:
            driver.quit()

if __name__ == "__main__":
    unittest.main()
