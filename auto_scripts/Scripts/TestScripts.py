# Existing content of TestScripts.py
# ... (existing test methods)

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from auto_scripts.Pages.LoginPage import LoginPage

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

    def test_tc_login_07_remember_me_session_persistence(self):
        """
        Test Case TC_LOGIN_07:
        1. Navigate to login page.
        2. Enter valid registered email and password.
        3. Check the 'Remember Me' option.
        4. Click on the 'Login' button.
        5. Close and reopen the browser, revisit the site, and verify session persists.
        """
        driver = webdriver.Chrome()
        page = LoginPage(driver)
        try:
            page.login_with_remember_me_and_validate_session(
                username='user1@example.com',
                password='ValidPassword123',
                home_url='https://example-ecommerce.com/',
                user_profile_locator=(By.CSS_SELECTOR, '.user-profile-name')
            )
        finally:
            try:
                driver.quit()
            except Exception:
                pass

    def test_tc020_cross_browser_login(self):
        """
        Test Case TC020:
        1. Attempt login on Chrome, Firefox, Safari, Edge, and mobile browsers.
        2. Test Data: user@example.com / ValidPassword123
        3. Acceptance Criteria: Login works as expected on all supported browsers/devices.
        """
        test_data = {'email': 'user@example.com', 'password': 'ValidPassword123'}
        results = LoginPage.login_on_all_supported_browsers(test_data)
        for browser, success in results.items():
            self.assertTrue(success, f"Login failed on {browser}")

if __name__ == "__main__":
    unittest.main()
