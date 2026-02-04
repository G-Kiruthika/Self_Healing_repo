# Test Script for TC_LOGIN_014: SQL Injection Login Attempt
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time

# Import the LoginPage Page Object
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope='function')
def driver():
    options = Options()
    options.add_argument('--headless')  # Remove if you want to see browser
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_with_sql_injection_payload_tc_login_014(driver):
    """
    TC_LOGIN_014: Attempt login with SQL injection payload in email field.
    Steps:
    1. Navigate to the login page [Test Data: URL: https://app.example.com/login]
    2. Enter SQL injection payload in email field [Test Data: Email: admin'--]
    3. Enter any password [Test Data: Password: anything]
    4. Click on the Login button
    5. Verify system security
    Expected:
        - Login fails with error message
        - SQL injection is prevented
        - No unauthorized access granted, system remains secure
    """
    login_page = LoginPage(driver)
    # Step 1: Navigate to login page
    login_page.go_to_login_page()
    assert driver.current_url.startswith(LoginPage.LOGIN_URL), "Login page did not load."
    assert login_page.is_login_fields_visible(), "Login fields not visible."

    # Step 2: Enter SQL injection payload in email field
    sql_injection_email = "admin'--"
    email_entered = login_page.enter_email(sql_injection_email)
    assert email_entered, f"Email field did not accept input: {sql_injection_email}"

    # Step 3: Enter any password
    test_password = "anything"
    password_masked = login_page.enter_password(test_password)
    assert password_masked, "Password field did not mask input."

    # Step 4: Click on the Login button
    login_page.click_login()
    time.sleep(1)  # Wait for response

    # Step 5: Verify error message is displayed, SQL injection is prevented, and no unauthorized access
    error_displayed = login_page.is_error_message_displayed()
    still_on_login_page = driver.current_url == LoginPage.LOGIN_URL
    unauthorized_access = not login_page.is_redirected_to_dashboard()

    assert error_displayed, "Error message not displayed after SQL injection attempt."
    assert still_on_login_page, "User was redirected from login page after SQL injection attempt."
    assert unauthorized_access, "Unauthorized access granted after SQL injection attempt!"
    print("TC_LOGIN_014 passed: SQL injection attempt was correctly handled.")
