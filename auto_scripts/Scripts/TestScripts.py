# Existing content of TestScripts.py
# ... (existing test methods)

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
    def test_tc_login_07_remember_me_session_persistence(self):
        ...
    def test_tc020_login_across_browsers(self):
        ...
    def test_tc_login_08_remember_me_session_not_persistent(self):
        ...
    def test_tc_login_09_forgot_password_navigation(self):
        ...
    def test_tc_login_017_password_masked_and_login_page_displayed(self):
        ...

    def test_tc_login_001_invalid_login_error_message(self):
        """
        Test Case TC_LOGIN_001:
        1. Navigate to the login screen.
        2. Enter invalid username and password.
        3. Click the login button.
        4. Assert error message is shown with text: 'Invalid username or password. Please try again.'
        """
        driver = webdriver.Chrome()
        page = LoginPage(driver)
        try:
            page.verify_invalid_login_shows_error('invalid@example.com', 'wrongpass')
        finally:
            driver.quit()

if __name__ == "__main__":
    unittest.main()
