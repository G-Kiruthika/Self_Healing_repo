# Test Script for TC_LOGIN_013 - SQL Injection Negative Login
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time

from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument('--headless')  # Comment this line if you want to see the browser
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_sql_injection(driver):
    """
    TC_LOGIN_013: Attempt login with SQL injection payload in email field.
    Steps:
    1. Navigate to the login page [Test Data: URL: https://app.example.com/login]
    2. Enter SQL injection payload in email field [Test Data: Email: admin'--]
    3. Enter any password [Test Data: Password: anything]
    4. Click on the Login button
    Expected: Login fails with error message, SQL injection is prevented, no unauthorized access granted.
    Acceptance Criteria: SCRUM-91
    """
    login_page = LoginPage(driver)

    # Step 1: Navigate to login page
    login_page.go_to_login_page()
    assert driver.current_url.startswith(LoginPage.LOGIN_URL), "Login page did not load."
    assert login_page.is_login_fields_visible(), "Login fields not visible."

    # Step 2: Enter SQL injection payload in email field
    sql_payload = "admin'--"
    assert login_page.enter_email(sql_payload), f"Failed to enter SQL payload: {sql_payload}"
    
    # Step 3: Enter any password
    password = "anything"
    assert login_page.enter_password(password), "Password field is not masked or not entered."

    # Step 4: Click Login button
    login_page.click_login()
    time.sleep(1)  # Small wait for response

    # Assert: Login fails, error message is displayed, SQL injection is prevented, no unauthorized access
    error_displayed = login_page.is_error_message_displayed()
    not_redirected = driver.current_url == LoginPage.LOGIN_URL
    unauthorized_access = not login_page.is_redirected_to_dashboard()
    
    assert error_displayed, "Error message not displayed after SQL injection attempt."
    assert not_redirected, "User was redirected after SQL injection, should remain on login page."
    assert unauthorized_access, "Unauthorized access was granted with SQL injection payload!"
    
    print("TC_LOGIN_013: SQL Injection negative login test passed.")
