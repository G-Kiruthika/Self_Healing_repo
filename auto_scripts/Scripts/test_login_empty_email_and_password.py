# Selenium Automation Test Script for TC_LOGIN_006: Both email and password fields empty
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import AssertionError, NoSuchElementException
import time
import sys
import os

# Import the LoginPage Page Object
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Pages.LoginPage import LoginPage

def get_webdriver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    return driver

@pytest.mark.login
@pytest.mark.negative
@pytest.mark.TC_LOGIN_006
def test_login_with_empty_email_and_empty_password():
    """
    TC_LOGIN_006: Attempt login with both email and password fields empty; verify validation errors for both fields are displayed.
    Steps:
    1. Navigate to the login page
    2. Leave both email and password fields empty
    3. Click Login button
    4. Verify validation errors 'Email is required' and 'Password is required' are displayed
    5. Verify user remains on login page
    """
    driver = get_webdriver()
    try:
        login_page = LoginPage(driver)

        # Step 1: Navigate to the login page
        login_page.go_to_login_page()
        assert driver.current_url == LoginPage.LOGIN_URL, f"Did not navigate to login page: {driver.current_url}"

        # Step 2: Leave both fields empty (ensure fields are empty)
        email_field = driver.find_element(*LoginPage.EMAIL_FIELD)
        email_field.clear()
        assert email_field.get_attribute("value") == "", "Email field is not empty!"
        password_field = driver.find_element(*LoginPage.PASSWORD_FIELD)
        password_field.clear()
        assert password_field.get_attribute("value") == "", "Password field is not empty!"

        # Step 3: Click Login button
        driver.find_element(*LoginPage.LOGIN_BUTTON).click()
        time.sleep(1)  # Wait for validation errors to appear

        # Step 4: Verify validation errors for both fields
        validation_errors = driver.find_elements(*LoginPage.VALIDATION_ERROR)
        assert validation_errors, "No validation errors found!"
        found_email_error = False
        found_password_error = False
        for error_elem in validation_errors:
            if error_elem.is_displayed():
                error_text = error_elem.text.lower()
                if "email is required" in error_text:
                    found_email_error = True
                if "password is required" in error_text:
                    found_password_error = True
        assert found_email_error, "Email required validation error not displayed!"
        assert found_password_error, "Password required validation error not displayed!"

        # Step 5: Verify user remains on login page
        assert driver.current_url == LoginPage.LOGIN_URL, "User is not on login page after failed login!"
    finally:
        driver.quit()
