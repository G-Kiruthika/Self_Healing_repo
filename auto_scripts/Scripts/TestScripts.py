import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from auto_scripts.Pages.LoginPage import LoginPage
from auto_scripts.Pages.PasswordRecoveryPage import PasswordRecoveryPage

class TestLoginPage(unittest.TestCase):
    # Existing test methods...
    ...
    def test_tc_login_06_empty_email_and_password_error(self):
        ...
    # ...other existing test methods...

    def test_tc_login_002_remember_me_checkbox_absence(self):
        ...

    def test_tc019_login_with_special_unicode_characters(self):
        ...

    def test_tc_login_001_invalid_login(self):
        """
        Test Case TC_LOGIN_001:
        1. Navigate to the login screen.
        2. Enter an invalid username and/or password.
        3. Verify error message 'Invalid username or password. Please try again.' is displayed.
        """
        driver = webdriver.Chrome()
        page = LoginPage(driver)
        try:
            email = "invalid@example.com"
            password = "wrongPassword"
            expected_error = "Invalid username or password. Please try again."
            page.perform_invalid_login_and_validate(email, password, expected_error)
        finally:
            driver.quit()

if __name__ == "__main__":
    unittest.main()
