# Test Script for TC_LOGIN_006: Attempt login with both email and password fields empty
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import sys
import os

# Import the LoginPage PageClass
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Pages.LoginPage import LoginPage

@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument('--headless')  # comment out if you want to see browser
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_login_with_empty_email_and_empty_password(driver):
    """
    TC_LOGIN_006: Attempt login with both email and password fields empty; verify validation errors for both fields are displayed.
    Steps:
    1. Navigate to the login page
    2. Leave both email and password fields empty
    3. Click Login button
    4. Verify validation errors 'Email is required' and 'Password is required' are displayed
    5. User remains on login page, login not attempted
    """
    login_page = LoginPage(driver)
    result = login_page.login_with_empty_email_and_empty_password()
    assert result is True, "TC_LOGIN_006 failed: Validation errors not displayed as expected or user was not prevented from logging in."
    # Additional explicit validation for traceability
    assert driver.current_url == LoginPage.LOGIN_URL, "User is not on login page after submitting empty credentials!"
    # Check both validation errors are present
    try:
        errors = driver.find_elements(*LoginPage.VALIDATION_ERROR)
        error_texts = [e.text.lower() for e in errors if e.is_displayed()]
        assert any("email is required" in t for t in error_texts), "Email required validation error not displayed!"
        assert any("password is required" in t for t in error_texts), "Password required validation error not displayed!"
    except NoSuchElementException:
        pytest.fail("Validation error elements not found!")
