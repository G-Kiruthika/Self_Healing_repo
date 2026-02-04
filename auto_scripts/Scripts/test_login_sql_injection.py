# Selenium Test Script for TC_LOGIN_013: SQL Injection Negative Test
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
import time

# Import the LoginPage Page Object
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope='function')
def driver():
    # Setup Chrome WebDriver (headless for CI, visible for local debug)
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_sql_injection_prevention(driver):
    """
    TC_LOGIN_013: Attempt login with SQL injection payload in email field.
    Steps:
      1. Navigate to the login page [Test Data: URL: https://app.example.com/login]
      2. Enter SQL injection payload in email field [Test Data: Email: admin'--]
      3. Enter any password [Test Data: Password: anything]
      4. Click on the Login button
    Acceptance Criteria:
      - Login fails with error message
      - SQL injection is prevented
      - No unauthorized access granted
    """
    login_page = LoginPage(driver)

    # Step 1: Navigate to login page
    login_page.go_to_login_page()
    assert driver.current_url.startswith(LoginPage.LOGIN_URL), "Login page URL mismatch."
    assert login_page.is_login_fields_visible(), "Login fields are not visible."

    # Step 2: Enter SQL injection payload in email field
    email_payload = "admin'--"
    email_entered = login_page.enter_email(email_payload)
    assert email_entered, "SQL injection payload was not entered in email field."

    # Step 3: Enter any password
    test_password = "anything"
    password_masked = login_page.enter_password(test_password)
    assert password_masked, "Password field is not masked or not entered."

    # Step 4: Click Login button
    login_page.click_login()
    time.sleep(1)  # Wait for login attempt and error message

    # Acceptance: Login fails, error shown, no unauthorized access
    error_displayed = login_page.is_error_message_displayed()
    unauthorized_access = login_page.is_redirected_to_dashboard()
    assert error_displayed, "No error message displayed after SQL injection attempt."
    assert not unauthorized_access, "Unauthorized access granted after SQL injection payload!"
    
    # Optionally, check error message text for generic login failure, not system error
    # (Assumes 'Invalid email or password' is the expected error)
    assert login_page.is_error_message_displayed("Invalid email or password"), (
        "Expected error message not displayed after SQL injection attempt."
    )

    print("TC_LOGIN_013: SQL Injection negative test passed.")
