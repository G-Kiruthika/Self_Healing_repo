# Test Script for TC_LOGIN_012 - Login with Email Exceeding Max Length
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage
import time

# Test data: Email exceeding 255 characters
OVERLONG_EMAIL = (
    "a123456789012345678901234567890123456789012345678901234567890123@"
    "b123456789012345678901234567890123456789012345678901234567890123."
    "c123456789012345678901234567890123456789012345678901234567890123."
    "d123456789012345678901234567890123456789012345678.comextra"
)

@pytest.fixture(scope='module')
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_login_with_email_exceeding_max_length(driver):
    """
    TC_LOGIN_012: Attempt to enter email address exceeding maximum length (255+ characters) and verify validation.
    1. Navigate to the login page
    2. Attempt to enter overlong email address
    3. Verify validation message or truncation
    """
    login_page = LoginPage(driver)
    login_page.go_to_login_page()
    # Step 1: Login page is displayed
    assert login_page.is_login_fields_visible(), "Login fields are not visible."
    # Step 2 & 3: Enter overlong email and verify truncation or error
    result = login_page.login_with_email_exceeding_max_length(OVERLONG_EMAIL)
    assert result, (
        "Either the input was not truncated to 255 chars, or the validation message 'Email exceeds maximum length' was not displayed. "
        "Please check the application validation logic and locators."
    )
    print("TC_LOGIN_012 passed: Email field correctly handles input exceeding max length.")
