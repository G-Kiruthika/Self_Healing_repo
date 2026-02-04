# test_login_TC_LOGIN_002.py
"""
Selenium Test Script for TC_LOGIN_002: Invalid Login Attempt
Covers:
  - Navigation to login page
  - Entering invalid credentials
  - Asserting error message
  - Verifying user remains on login page
Traceability: testCaseId=118
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from auto_scripts.Pages.LoginPage import LoginPage
import time

# Test Data
LOGIN_URL = "https://app.example.com/login"
INVALID_EMAIL = "invaliduser@example.com"
VALID_PASSWORD = "ValidPass123!"
EXPECTED_ERROR_MESSAGE = "Invalid email or password"

@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_with_invalid_credentials_TC_LOGIN_002(driver):
    """
    Test Case: TC_LOGIN_002
    Steps:
    1. Navigate to the login page
    2. Enter invalid email address
    3. Enter valid password
    4. Click on the Login button
    5. Verify error message is displayed and user remains on login page
    """
    login_page = LoginPage(driver)

    # Step 1: Navigate to login page
    login_page.go_to_login_page()
    assert driver.current_url == LOGIN_URL, f"Expected URL {LOGIN_URL}, got {driver.current_url}"
    assert login_page.is_login_fields_visible(), "Login fields are not visible on the page."

    # Step 2: Enter invalid email address
    assert login_page.enter_email(INVALID_EMAIL), f"Email field did not accept value: {INVALID_EMAIL}"

    # Step 3: Enter valid password
    assert login_page.enter_password(VALID_PASSWORD), "Password field is not masked or did not accept value."

    # Step 4: Click Login
    login_page.click_login()

    # Wait for error message or page update
    time.sleep(1)

    # Step 5: Assert error message is displayed
    assert login_page.is_error_message_displayed(EXPECTED_ERROR_MESSAGE), (
        f"Expected error message '{EXPECTED_ERROR_MESSAGE}' not displayed after invalid login."
    )

    # Step 6: Verify user remains on login page and is not authenticated
    assert login_page.verify_user_remains_on_login_page(), (
        "User is not on login page or may have been authenticated unexpectedly."
    )

    # Extra: Ensure session token is not created
    assert not login_page.is_session_token_created(), "Session token should not be created for invalid login."
