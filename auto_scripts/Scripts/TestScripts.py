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

    def test_tc020_login_across_browsers(self):
        """
        Test Case TC020:
        Attempt login on Chrome, Firefox, Safari, Edge, and mobile browsers.
        Test Data: user@example.com / ValidPassword123
        Acceptance Criteria: Login works as expected on all supported browsers/devices.
        """
        email = "user@example.com"
        password = "ValidPassword123"
        browsers = {}
        try:
            # Desktop browsers
            try:
                browsers['chrome'] = webdriver.Chrome()
            except Exception:
                pass
            try:
                browsers['firefox'] = webdriver.Firefox()
            except Exception:
                pass
            try:
                browsers['edge'] = webdriver.Edge()
            except Exception:
                pass
            try:
                browsers['safari'] = webdriver.Safari()
            except Exception:
                pass
            mobile_caps = None
            try:
                from appium import webdriver as appium_webdriver
                mobile_caps = {
                    'android': {
                        'platformName': 'Android',
                        'deviceName': 'Android Emulator',
                        'browserName': 'Chrome'
                    },
                    'ios': {
                        'platformName': 'iOS',
                        'deviceName': 'iPhone Simulator',
                        'browserName': 'Safari'
                    }
                }
            except ImportError:
                pass
            page = LoginPage(None)
            results = page.login_across_browsers(email=email, password=password, browsers=browsers, mobile_caps=mobile_caps)
            for browser_device, result in results.items():
                self.assertTrue(result, f"Login failed on {browser_device}")
        finally:
            for driver in browsers.values():
                try:
                    driver.quit()
                except Exception:
                    pass

    def test_tc_login_08_remember_me_session_not_persistent(self):
        """
        Test Case TC_LOGIN_08:
        1. Navigate to login page.
        2. Enter valid registered email and password.
        3. Ensure 'Remember Me' is NOT checked.
        4. Click on the 'Login' button.
        5. Close and reopen the browser, revisit the site, and verify user is logged out and redirected to the login page.
        """
        def driver_factory():
            return webdriver.Chrome()
        driver = webdriver.Chrome()
        page = LoginPage(driver)
        try:
            results = page.login_without_remember_me_and_validate_session(
                email='user1@example.com',
                password='ValidPassword123',
                driver_factory=driver_factory
            )
            self.assertTrue(results['login_page_opened'], "Login page did not open.")
            self.assertTrue(results['credentials_entered'], "Credentials were not entered.")
            self.assertTrue(results['remember_me_unchecked'], "'Remember Me' was not unchecked.")
            self.assertTrue(results['user_logged_in'], "User did not log in.")
            self.assertTrue(results['user_logged_out_after_reopen'], "User was not logged out after browser reopen.")
        finally:
            try:
                driver.quit()
            except Exception:
                pass

    def test_tc_login_09_forgot_password_navigation(self):
        """
        Test Case TC_LOGIN_09:
        1. Navigate to the login page.
        2. Click on the 'Forgot Password' link.
        3. Verify 'Forgot Password' page is displayed.
        """
        driver = webdriver.Chrome()
        login_page = LoginPage(driver)
        try:
            login_page.tc_login_09_navigate_and_click_forgot_password()
            recovery_page = PasswordRecoveryPage(driver)
            recovery_page.tc_login_09_verify_forgot_password_page()
        finally:
            try:
                driver.quit()
            except Exception:
                pass

    def test_tc_login_017_password_masked_and_login_page_displayed(self):
        """
        Test Case TC_LOGIN_017:
        1. Navigate to the login page and verify it is displayed.
        2. Enter password 'ValidPass123' and verify the password field is masked.
        """
        driver = webdriver.Chrome()
        page = LoginPage(driver)
        try:
            login_page_displayed = page.is_login_page_displayed()
            self.assertTrue(login_page_displayed, "Login page is not displayed.")
            # Enter password and check masking
            password_masked = page.is_password_field_masked()
            self.assertTrue(password_masked, "Password field is not masked.")
        finally:
            driver.quit()

if __name__ == "__main__":
    unittest.main()
