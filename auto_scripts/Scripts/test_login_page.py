# Selenium Test Script for LoginPage automation
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from auto_scripts.Pages.LoginPage import LoginPage
import time

# Test Data
VALID_EMAIL = "testuser@example.com"
VALID_PASSWORD = "ValidPass123!"
INVALID_EMAIL = "invaliduser@example.com"
INVALID_PASSWORD = "WrongPass!"

@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    try:
        driver.quit()
    except WebDriverException:
        pass

# Utility factory for session persistence test
def driver_factory():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    new_driver = webdriver.Chrome(options=options)
    new_driver.implicitly_wait(5)
    return new_driver

class TestLoginPage:
    def test_login_successful(self, driver):
        """
        TC_LOGIN_001: End-to-end login workflow with valid credentials.
        """
        login_page = LoginPage(driver)
        result = login_page.login_successful(VALID_EMAIL, VALID_PASSWORD)
        assert result is True, "Login with valid credentials failed."

    def test_login_with_invalid_email_valid_password(self, driver):
        """
        TC_LOGIN_002: Attempt login with invalid email and valid password.
        """
        login_page = LoginPage(driver)
        result = login_page.login_with_invalid_email_valid_password(INVALID_EMAIL, VALID_PASSWORD)
        assert result is True, "Login with invalid email did not behave as expected."

    def test_login_with_valid_email_invalid_password(self, driver):
        """
        TC_LOGIN_003: Attempt login with valid email and invalid password.
        """
        login_page = LoginPage(driver)
        result = login_page.login_with_valid_email_invalid_password(VALID_EMAIL, INVALID_PASSWORD)
        assert result is True, "Login with invalid password did not behave as expected."

    def test_login_with_empty_email_and_valid_password(self, driver):
        """
        TC_LOGIN_004: Attempt login with empty email and valid password.
        """
        login_page = LoginPage(driver)
        result = login_page.login_with_empty_email_and_valid_password(VALID_PASSWORD)
        assert result is True, "Login with empty email did not show correct validation error."

    def test_login_with_valid_email_and_empty_password(self, driver):
        """
        TC_LOGIN_005: Attempt login with valid email and empty password.
        """
        login_page = LoginPage(driver)
        result = login_page.login_with_valid_email_and_empty_password(VALID_EMAIL)
        assert result is True, "Login with empty password did not show correct validation error."

    def test_login_with_empty_email_and_empty_password(self, driver):
        """
        TC_LOGIN_006: Attempt login with both email and password fields empty.
        """
        login_page = LoginPage(driver)
        result = login_page.login_with_empty_email_and_empty_password()
        assert result is True, "Login with both fields empty did not show correct validation errors."

    def test_remember_me_session_persistence(self):
        """
        TC_LOGIN_007: End-to-end test for 'Remember Me' session persistence after browser restart.
        """
        # Initial driver for login
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(5)
        login_page = LoginPage(driver)
        result = login_page.remember_me_session_persistence(VALID_EMAIL, VALID_PASSWORD, driver_factory)
        driver.quit()
        assert result is True, "Session did not persist after browser restart with 'Remember Me'."
