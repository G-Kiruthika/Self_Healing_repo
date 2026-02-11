# Existing imports
from selenium import webdriver
import pytest
from auto_scripts.PageObjects.LoginPage import LoginPage
from auto_scripts.PageObjects.DashboardPage import DashboardPage

# Existing test functions...
# (Assume all previous code is preserved here)

def test_tc_login_001_valid_credentials():
    """
    TC_LOGIN_001: Valid Login
    Steps:
        1. Navigate to login page (https://ecommerce.example.com/login)
        2. Enter valid username (validuser@example.com)
        3. Enter valid password (ValidPass123!)
        4. Click Login
        5. Validate dashboard/home page displayed and session established
    """
    driver = webdriver.Chrome()
    try:
        driver.get("https://ecommerce.example.com/login")
        login_page = LoginPage(driver)
        login_page.enter_username("validuser@example.com")
        login_page.enter_password("ValidPass123!")
        login_page.click_login()

        dashboard_page = DashboardPage(driver)
        assert dashboard_page.is_displayed(), "Dashboard page was not displayed after login."
        assert dashboard_page.is_session_active(), "Session was not established after login."
    finally:
        driver.quit()


def test_tc_login_002_invalid_credentials():
    """
    TC_LOGIN_002: Invalid Login Attempt
    Steps:
        1. Navigate to login page (https://ecommerce.example.com/login)
        2. Enter invalid username (invaliduser@example.com)
        3. Enter valid password (ValidPass123!)
        4. Click Login
        5. Validate error message 'Invalid username or password' is displayed and user remains on login page
    """
    driver = webdriver.Chrome()
    try:
        login_page = LoginPage(driver)
        result = login_page.perform_invalid_login_and_validate("invaliduser@example.com", "ValidPass123!")
        assert result["error_message"] is not None, "Error message not found after invalid login."
        assert "Invalid username or password" in result["error_message"], f"Expected error 'Invalid username or password', got '{result["error_message"]}'"
        assert result["on_login_page"], "User is not on login page after failed login."
    finally:
        driver.quit()


def test_tc_login_003_valid_username_invalid_password():
    """
    TC_LOGIN_003: Valid Username, Invalid Password
    Steps:
        1. Navigate to login page (https://ecommerce.example.com/login)
        2. Enter valid username (validuser@example.com)
        3. Enter invalid password (WrongPass456!)
        4. Click Login
        5. Validate error message 'Invalid username or password' is displayed and user remains on login page
    """
    driver = webdriver.Chrome()
    try:
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.enter_username("validuser@example.com")
        login_page.enter_password("WrongPass456!")
        login_page.click_login()
        login_page.validate_error_message("Invalid username or password")
    finally:
        driver.quit()


def test_tc_login_004_empty_username_valid_password():
    """
    TC_LOGIN_004: Negative login scenario (empty username, valid password)
    Steps:
        1. Navigate to login page (https://ecommerce.example.com/login)
        2. Leave username field empty
        3. Enter valid password ('ValidPass123!')
        4. Click Login
        5. Validate error message 'Username is required' is displayed and user remains on login page
    """
    driver = webdriver.Chrome()
    try:
        login_page = LoginPage(driver)
        result = login_page.perform_empty_username_login_and_validate("ValidPass123!")
        # Accept both error and validation error, as UI may use either
        error_msg = result.get('error_message')
        validation_msg = result.get('validation_error')
        assert (
            error_msg and 'Username is required' in error_msg
        ) or (
            validation_msg and 'Username is required' in validation_msg
        ), f"Expected error 'Username is required', got error='{error_msg}', validation='{validation_msg}'"
        assert result.get('on_login_page'), 'User is not on login page after failed login.'
    finally:
        driver.quit()
