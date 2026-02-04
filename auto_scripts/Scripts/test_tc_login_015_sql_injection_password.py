# Selenium Test Script for TC_LOGIN_015: SQL Injection in Password Field
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
import time

# Import the LoginPage Page Object
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope='function')
def driver():
    # Setup Chrome WebDriver (headless for CI/CD)
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    try:
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(10)
        yield driver
    finally:
        driver.quit()

def test_tc_login_015_sql_injection_password(driver):
    """
    TC_LOGIN_015: Attempt SQL injection in the password field and verify that login fails, error message is displayed, and no unauthorized access is granted.
    Steps:
    1. Navigate to the login page
    2. Enter valid email address
    3. Enter SQL injection payload in password field
    4. Click Login button
    5. Assert error message is displayed, login fails, and user is not redirected to dashboard
    """
    # Test Data
    valid_email = 'testuser@example.com'
    sql_injection_password = "' OR '1'='1"

    login_page = LoginPage(driver)

    # Step 1: Navigate to the login page
    login_page.go_to_login_page()
    assert driver.current_url.startswith(LoginPage.LOGIN_URL), "Did not reach login page URL."
    assert login_page.is_login_fields_visible(), "Login fields are not visible."

    # Step 2: Enter valid email address
    email_entered = login_page.enter_email(valid_email)
    assert email_entered, f"Email '{valid_email}' was not entered correctly."

    # Step 3: Enter SQL injection payload in password field
    password_entered = login_page.enter_password(sql_injection_password)
    assert password_entered, "Password field is not accepting input or is not masked."

    # Step 4: Click Login button
    login_page.click_login()
    time.sleep(1)  # Allow time for page response

    # Step 5: Assert error message is displayed, login fails, and user is not redirected
    error_displayed = login_page.is_error_message_displayed()
    still_on_login_page = driver.current_url == LoginPage.LOGIN_URL
    unauthorized_access = not login_page.is_redirected_to_dashboard()

    assert error_displayed, "Error message not displayed after SQL injection attempt."
    assert still_on_login_page, "User was redirected away from login page after SQL injection attempt."
    assert unauthorized_access, "Unauthorized access granted after SQL injection attempt."

    print("TC_LOGIN_015 passed: SQL injection in password field is prevented and handled securely.")
