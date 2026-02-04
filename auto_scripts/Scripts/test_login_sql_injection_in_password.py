# Test Script for TC_LOGIN_015: SQL Injection in Password Field
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from auto_scripts.Pages.LoginPage import LoginPage
import time

@pytest.fixture(scope='module')
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_login_with_sql_injection_in_password(driver):
    """
    TC_LOGIN_015: Attempt SQL injection in password field and verify application is not vulnerable.
    Steps:
    1. Navigate to the login page [Test Data: URL: https://app.example.com/login]
    2. Enter valid email address [Test Data: Email: testuser@example.com]
    3. Enter SQL injection payload in password field [Test Data: Password: ' OR '1'='1]
    4. Click on the Login button
    5. Verify:
        - Input is masked and entered
        - Login fails with error message
        - SQL injection is prevented
        - No unauthorized access
    Acceptance Criteria: SCRUM-91
    """
    login_page = LoginPage(driver)
    email = "testuser@example.com"
    sql_password = "' OR '1'='1"

    # Step 1: Navigate to the login page
    login_page.go_to_login_page()
    assert driver.current_url.startswith(LoginPage.LOGIN_URL), "Login page did not load!"

    # Step 2: Enter valid email address
    assert login_page.enter_email(email), "Email was not entered correctly!"

    # Step 3: Enter SQL injection payload in password field
    assert login_page.enter_password(sql_password), "SQL injection payload was not entered/masked correctly!"
    password_field = driver.find_element(*LoginPage.PASSWORD_FIELD)
    assert password_field.get_attribute("type") == "password", "Password field is not masked!"

    # Step 4: Click on the Login button
    login_page.click_login()
    time.sleep(1)  # Allow time for error message to appear

    # Step 5: Verify error message is displayed
    error_message = login_page.get_error_message()
    assert error_message is not None, "No error message displayed!"
    assert driver.current_url == LoginPage.LOGIN_URL, "User is not on login page after SQL injection attempt!"
    assert not login_page.is_redirected_to_dashboard(), "Unauthorized access granted after SQL injection!"
    assert "sql" not in error_message.lower(), "SQL error message leaked to user!"
    # Ensure password field is still masked
    password_field = driver.find_element(*LoginPage.PASSWORD_FIELD)
    assert password_field.get_attribute("type") == "password", "Password field is not masked after login attempt!"
