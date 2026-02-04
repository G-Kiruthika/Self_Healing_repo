# Selenium test script for TC_LOGIN_015: SQL Injection in Password Field
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import sys
import os

# Adjust sys.path to import LoginPage from Pages
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../Pages')))
from LoginPage import LoginPage

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

def test_login_with_sql_injection_in_password(driver):
    """
    TC_LOGIN_015: Attempt SQL injection in password field and verify application is not vulnerable.
    Steps:
    1. Navigate to the login page [Test Data: URL: https://app.example.com/login]
    2. Enter valid email address [Test Data: Email: testuser@example.com]
    3. Enter SQL injection payload in password field [Test Data: Password: ' OR '1'='1]
    4. Click on the Login button
    5. Verify login fails with error message, SQL injection is prevented, no unauthorized access
    Acceptance Criteria: SCRUM-91
    """
    login_page = LoginPage(driver)
    email = "testuser@example.com"
    sql_password = "' OR '1'='1"

    # Step 1: Navigate to login page
    login_page.go_to_login_page()
    assert driver.current_url.startswith("https://app.example.com/login"), "Login page URL is incorrect!"

    # Step 2: Enter valid email
    assert login_page.is_login_fields_visible(), "Login fields are not visible!"
    assert login_page.enter_email(email), "Email was not entered correctly!"

    # Step 3: Enter SQL injection payload in password field
    assert login_page.enter_password(sql_password), "SQL injection payload was not entered/masked correctly!"
    password_field = driver.find_element(By.ID, "login-password")
    assert password_field.get_attribute("type") == "password", "Password field is not masked!"

    # Step 4: Click Login button
    login_page.click_login()
    time.sleep(1)  # Wait for error message

    # Step 5: Verify login fails, error message, SQL injection prevented, no unauthorized access
    error_message = login_page.get_error_message()
    assert error_message is not None, "No error message displayed!"
    assert driver.current_url.startswith(login_page.LOGIN_URL), "User is not on login page after SQL injection attempt!"
    assert not login_page.is_redirected_to_dashboard(), "Unauthorized access granted after SQL injection!"
    assert "sql" not in error_message.lower(), "SQL error message leaked to user!"

    # Ensure password field is still masked
    password_field = driver.find_element(By.ID, "login-password")
    assert password_field.get_attribute("type") == "password", "Password field is not masked after login attempt!"

    print("TC_LOGIN_015 passed: SQL injection in password field is safely handled.")
