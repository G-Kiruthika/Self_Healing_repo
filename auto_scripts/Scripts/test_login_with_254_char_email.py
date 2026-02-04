# -*- coding: utf-8 -*-
"""
Selenium Automation Test Script for TC_LOGIN_011: Login with 254-character Email
Author: Automation Agent
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from auto_scripts.Pages.LoginPage import LoginPage
import time

# Test data for TC_LOGIN_011
MAX_LENGTH_EMAIL = (
    "a123456789012345678901234567890123456789012345678901234567890123@"
    "b123456789012345678901234567890123456789012345678901234567890123."
    "c123456789012345678901234567890123456789012345678901234567890123."
    "d123456789012345678901234567890123456789012345678.com"
)
VALID_PASSWORD = "ValidPass123!"
LOGIN_URL = "https://app.example.com/login"

@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_with_254_char_email(driver):
    """
    TC_LOGIN_011: Enter email address at maximum allowed length (254 characters), valid password, and attempt login.
    Steps:
    1. Navigate to the login page
    2. Enter email address at maximum allowed length (254 characters)
    3. Enter valid password
    4. Click on the Login button
    5. Verify email is accepted and entered, password is entered and masked, login attempt is processed without validation error.
    """
    login_page = LoginPage(driver)

    # Step 1: Navigate to the login page
    login_page.go_to_login_page()
    assert driver.current_url == LOGIN_URL, "Login page URL mismatch!"
    assert login_page.is_login_fields_visible(), "Login fields are not visible!"

    # Step 2: Enter 254-char email
    assert len(MAX_LENGTH_EMAIL) == 254, f"Test email is not 254 chars: {len(MAX_LENGTH_EMAIL)}"
    assert login_page.enter_email(MAX_LENGTH_EMAIL), "Email was not entered correctly!"
    entered_email = driver.find_element(*login_page.EMAIL_FIELD).get_attribute("value")
    assert entered_email == MAX_LENGTH_EMAIL, "Entered email does not match test data!"

    # Step 3: Enter valid password
    assert login_page.enter_password(VALID_PASSWORD), "Password was not entered/masked correctly!"
    password_field_type = driver.find_element(*login_page.PASSWORD_FIELD).get_attribute("type")
    assert password_field_type == "password", "Password field is not masked!"

    # Step 4: Click Login
    login_page.click_login()

    # Step 5: Wait for response and check for validation errors
    time.sleep(1)
    error_message = login_page.get_error_message()
    assert not error_message, f"Unexpected error message after login attempt: {error_message}"

    # Optionally, check that user is not erroneously rejected for email length
    # (If success redirects to dashboard, check for that. If not, ensure no validation error.)
    # The actual post-login state may depend on environment.
