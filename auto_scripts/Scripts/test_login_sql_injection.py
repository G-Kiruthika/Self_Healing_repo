# Selenium Test Script for TC_LOGIN_013: SQL Injection in Login Email Field
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import os
import sys

# Ensure the Pages module is importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Pages.LoginPage import LoginPage

@pytest.fixture(scope='module')
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_login_with_sql_injection_in_email(driver):
    """
    TC_LOGIN_013: Attempt SQL injection in email field and verify no unauthorized access is granted.
    Acceptance Criteria: SCRUM-91
    Steps:
    1. Navigate to the login page [Test Data: URL: https://app.example.com/login]
    2. Enter SQL injection payload in email field [Test Data: Email: admin'--]
    3. Enter any password [Test Data: Password: anything]
    4. Click on the Login button
    Expected: Login fails with error message, SQL injection is prevented, no unauthorized access granted.
    """
    login_page = LoginPage(driver)
    sql_payload = "admin'--"
    password = "anything"
    # Step 1: Navigate to login page
    login_page.go_to_login_page()
    assert driver.current_url.startswith("https://app.example.com/login"), "Login page URL mismatch!"
    # Step 2: Enter SQL injection payload in email field
    assert login_page.enter_email(sql_payload), "SQL injection payload was not entered correctly!"
    # Step 3: Enter any password
    assert login_page.enter_password(password), "Password was not entered/masked correctly!"
    # Step 4: Click Login
    login_page.click_login()
    time.sleep(1)  # Wait for error message
    error_message = login_page.get_error_message()
    assert error_message is not None, "No error message displayed!"
    # Check that we are still on login page and not redirected
    assert driver.current_url.startswith(login_page.LOGIN_URL), "User is not on login page after SQL injection attempt!"
    # Optionally, check that error message does not reveal SQL or internal details
    assert "sql" not in error_message.lower(), f"Error message reveals SQL details: {error_message}"
    assert "syntax" not in error_message.lower(), f"Error message reveals SQL syntax: {error_message}"
    # Negative check: ensure dashboard is NOT visible
    try:
        dashboard_header = driver.find_element(By.CSS_SELECTOR, "h1.dashboard-title")
        assert not dashboard_header.is_displayed(), "Dashboard header should NOT be visible after failed login!"
    except NoSuchElementException:
        pass  # This is expected
    # Negative check: ensure user profile is NOT visible
    try:
        user_icon = driver.find_element(By.CSS_SELECTOR, ".user-profile-name")
        assert not user_icon.is_displayed(), "User profile should NOT be visible after failed login!"
    except NoSuchElementException:
        pass  # This is expected
    # Traceability
    print("[TC_LOGIN_013] SQL injection negative test completed successfully.")
