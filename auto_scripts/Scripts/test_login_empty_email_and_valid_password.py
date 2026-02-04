#!/usr/bin/env python3
"""
Test Script for TC_LOGIN_006: Attempt login with both email and password fields empty; verify validation errors for both fields are displayed.

Test Steps:
1. Navigate to the login page
2. Leave both email and password fields empty
3. Click Login button
4. Verify validation errors 'Email is required' and 'Password is required' are displayed

Acceptance Criteria:
- Validation errors for both email and password fields are shown when both are empty.
- User remains on login page and is not authenticated.

Author: Automated Generator
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time

from auto_scripts.Pages.LoginPage import LoginPage

def get_chrome_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    return driver

@pytest.mark.login
@pytest.mark.negative
class TestLoginEmptyFields:
    def setup_method(self):
        self.driver = get_chrome_driver()
        self.login_page = LoginPage(self.driver)

    def teardown_method(self):
        if self.driver:
            self.driver.quit()

    def test_login_with_empty_email_and_empty_password(self):
        """
        TC_LOGIN_006: Attempt login with both email and password fields empty; verify validation errors for both fields are displayed.
        """
        self.login_page.go_to_login_page()
        assert self.login_page.is_login_fields_visible(), "Login fields are not visible!"
        # Leave both fields empty
        email_field = self.driver.find_element(*self.login_page.EMAIL_FIELD)
        email_field.clear()
        assert email_field.get_attribute("value") == "", "Email field is not empty!"
        password_field = self.driver.find_element(*self.login_page.PASSWORD_FIELD)
        password_field.clear()
        assert password_field.get_attribute("value") == "", "Password field is not empty!"
        self.login_page.click_login()
        time.sleep(1)  # Wait for validation errors
        try:
            validation_errors = self.driver.find_elements(*self.login_page.VALIDATION_ERROR)
            assert validation_errors, "No validation errors found!"
            found_email_error = False
            found_password_error = False
            for error_elem in validation_errors:
                if error_elem.is_displayed():
                    error_text = error_elem.text.lower()
                    if "email is required" in error_text or "username is required" in error_text or "please enter username" in error_text:
                        found_email_error = True
                    if "password is required" in error_text:
                        found_password_error = True
            assert found_email_error, "Email/Username required validation error not displayed!"
            assert found_password_error, "Password required validation error not displayed!"
            # User should remain on login page
            assert self.driver.current_url == self.login_page.LOGIN_URL, "User is not on login page after failed login!"
        except NoSuchElementException:
            pytest.fail("Validation error elements not found!")
