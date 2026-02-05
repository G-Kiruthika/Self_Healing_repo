"""
Selenium Test Script for TC_SCRUM74_007: Login with both fields empty
Covers acceptance criteria AC_006
Author: Automation Agent
"""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope='module')
def driver():
    options = Options()
    options.add_argument('--headless')  # Remove if GUI needed
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_login_with_empty_fields(driver):
    """
    TC_SCRUM74_007: Login with both fields empty
    Steps:
    1. Navigate to the login page
    2. Leave email/username field empty
    3. Leave password field empty
    4. Click on the Login button
    5. Verify validation errors displayed for both fields: 'Email/Username and Password are required'
    """
    login_page = LoginPage(driver)
    result = login_page.tc_scrum74_007_empty_fields_validation()

    # Assert navigation succeeded
    assert result.get('navigate_to_login', False), f"Navigation failed: {result.get('error', '')}"
    # Assert email field handled
    assert result.get('enter_email', False), f"Email field error: {result.get('error', '')}"
    # Assert password field handled
    assert result.get('enter_password', False), f"Password field error: {result.get('error', '')}"
    # Assert login button clicked
    assert result.get('click_login', False), f"Login button error: {result.get('error', '')}"
    # Assert validation error is displayed
    assert result.get('validation_error_displayed', False), (
        "Validation error for empty fields not displayed as expected. "
        f"Result: {result}"
    )
    print("Test Case TC_SCRUM74_007 passed: Validation error displayed for empty fields.")
