# Selenium Test Script for TC_LOGIN_016: XSS Script Payload in Email Field
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoAlertPresentException, WebDriverException
import time
import os
import sys

# Ensure the Pages directory is in the path for import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../Pages')))
from LoginPage import LoginPage

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_login_with_xss_script_payload(driver):
    """
    TC_LOGIN_016: Attempt login with XSS script payload in email field and verify input is sanitized or rejected and no script execution occurs.
    Steps:
    1. Navigate to the login page [Test Data: URL: https://app.example.com/login] [Acceptance Criteria: AC_008]
    2. Enter XSS script payload in email field [Test Data: Email: <script>alert('XSS')</script>@test.com] [Acceptance Criteria: AC_008]
    3. Enter any password [Test Data: Password: TestPass123] [Acceptance Criteria: AC_008]
    4. Click on the Login button [Test Data: N/A] [Acceptance Criteria: AC_008]
    5. Verify no script execution [Test Data: N/A] [Acceptance Criteria: AC_008]
    Expected:
    - Input is sanitized or rejected
    - No alert popup or script execution occurs
    - System remains secure
    """
    login_page = LoginPage(driver)
    email_xss_payload = "<script>alert('XSS')</script>@test.com"
    password = "TestPass123"

    # Step 1: Navigate to the login page
    login_page.go_to_login_page()
    assert driver.current_url.startswith(LoginPage.LOGIN_URL), "Did not navigate to login page!"

    # Step 2: Enter XSS script payload in email field
    assert login_page.enter_email(email_xss_payload), "XSS payload was not entered correctly!"

    # Step 3: Enter any password
    assert login_page.enter_password(password), "Password was not entered/masked correctly!"

    # Step 4: Click on the Login button
    login_page.click_login()
    time.sleep(1)  # Wait for possible error message or alert

    # Step 5: Verify no script execution (no alert popup)
    try:
        alert = driver.switch_to.alert
        alert_text = alert.text
        alert.dismiss()
        pytest.fail(f"Unexpected alert popup detected: {alert_text}")
    except (NoAlertPresentException, WebDriverException):
        # No alert found, which is expected
        pass

    # Check that input is sanitized or rejected (error message shown)
    error_message = login_page.get_error_message()
    assert error_message is not None, "No error message displayed for XSS payload!"
    assert (
        "invalid" in error_message.lower() or
        "error" in error_message.lower() or
        "not allowed" in error_message.lower() or
        "sanitized" in error_message.lower()
    ), f"Unexpected error message: {error_message}"

    # Ensure user is not redirected to dashboard
    assert driver.current_url == LoginPage.LOGIN_URL, "User is not on login page after XSS payload!"
    assert not login_page.is_redirected_to_dashboard(), "Unauthorized access granted after XSS payload!"
