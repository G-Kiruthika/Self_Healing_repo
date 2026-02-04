# Test Script for TC_LOGIN_014: SQL Injection in Login (Email Field)
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
import time

from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1440, 900)
    yield driver
    driver.quit()

def test_TC_LOGIN_014_sql_injection_email(driver):
    """
    TC_LOGIN_014: Attempt login with SQL injection payload in email field.
    Steps:
        1. Navigate to the login page
        2. Enter SQL injection payload in email field (admin'--)
        3. Enter any password (anything)
        4. Click on the Login button
        5. Verify login fails with error message, SQL injection is prevented, and no unauthorized access is granted.
    Acceptance Criteria (AC_008):
        - Login page is displayed
        - Input is entered
        - Password is entered
        - Login fails with error message, SQL injection is prevented
        - No unauthorized access granted, system remains secure
    """
    login_page = LoginPage(driver)
    # Step 1: Navigate to login page
    login_page.go_to_login_page()
    assert driver.current_url == LoginPage.LOGIN_URL, "Did not navigate to login page."
    assert login_page.is_login_fields_visible(), "Login fields are not visible."

    # Step 2: Enter SQL injection payload in email field
    sql_injection_email = "admin'--"
    email_entered = login_page.enter_email(sql_injection_email)
    assert email_entered, f"SQL injection payload '{sql_injection_email}' was not entered in email field."

    # Step 3: Enter any password
    test_password = "anything"
    password_entered = login_page.enter_password(test_password)
    assert password_entered, "Password was not entered or not masked."

    # Step 4: Click on Login button
    login_page.click_login()
    time.sleep(1)  # Wait for error message or redirect

    # Step 5: Validation
    error_displayed = login_page.is_error_message_displayed()
    assert error_displayed, "Error message for failed login not displayed. SQL injection may not be prevented."
    still_on_login_page = driver.current_url == LoginPage.LOGIN_URL
    assert still_on_login_page, "User was redirected away from login page after SQL injection attempt."
    unauthorized_access = not login_page.is_redirected_to_dashboard()
    assert unauthorized_access, "Unauthorized access granted after SQL injection attempt!"

    # Final assertion using PageClass method for traceability
    assert login_page.login_with_sql_injection_email(sql_injection_email, test_password), (
        "login_with_sql_injection_email() did not return True: SQL injection protection failed or criteria not met."
    )
