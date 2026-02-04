# Selenium Automation Test Script for TC_LOGIN_014 - SQL Injection Security
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_sql_injection_security(driver):
    """
    Test Case: TC_LOGIN_014
    Title: Attempt login with SQL injection payload in email field and verify security.
    Steps:
        1. Navigate to the login page
        2. Enter SQL injection payload in email field (admin'--)
        3. Enter any password (e.g., 'anything')
        4. Click on the Login button
        5. Verify login fails, SQL injection is prevented, and no unauthorized access is granted
    Acceptance Criteria:
        - Login fails with error message
        - SQL injection is prevented
        - No unauthorized access granted, system remains secure
    """
    login_page = LoginPage(driver)
    sql_injection_payload = "admin'--"
    password = "anything"

    # Step 1: Navigate to the login page
    login_page.go_to_login_page()
    assert driver.current_url.startswith("https://app.example.com/login"), "Did not land on the login page."
    assert login_page.is_login_fields_visible(), "Login fields are not visible!"

    # Step 2: Enter SQL injection payload in email field
    assert login_page.enter_email(sql_injection_payload), "SQL injection payload was not entered correctly!"

    # Step 3: Enter any password
    assert login_page.enter_password(password), "Password was not entered/masked correctly!"

    # Step 4: Click on the Login button
    login_page.click_login()
    time.sleep(1)

    # Step 5: Verify login fails, SQL injection is prevented, error message is shown, no unauthorized access
    error_message = login_page.get_error_message()
    assert error_message is not None, "No error message displayed!"
    assert ("invalid" in error_message.lower() or "error" in error_message.lower()), f"Unexpected error message: {error_message}"
    assert driver.current_url == login_page.LOGIN_URL, "User is not on login page after failed login!"
    assert not login_page.is_redirected_to_dashboard(), "Unauthorized access granted! SQL injection not prevented."
