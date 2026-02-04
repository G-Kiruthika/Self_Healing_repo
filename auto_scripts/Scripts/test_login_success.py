# test_login_success.py
# Selenium Test Script for TC_LOGIN_001: Successful Login
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import sys
import os

# Ensure Page Object import works regardless of working directory
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

def test_TC_LOGIN_001_successful_login(driver):
    """
    Test Case: TC_LOGIN_001
    Description: Perform login with valid credentials and verify successful login and session creation.
    Steps:
        1. Navigate to the login page
        2. Enter valid username in the username field
        3. Enter valid password in the password field
        4. Click on the Login button
        5. Verify user session is created and user details are displayed
    Acceptance Criteria: AC_001_Successful_Login
    """
    # Test Data
    email = "testuser@example.com"
    password = "Test@1234"
    login_page = LoginPage(driver)

    # Step 1: Navigate to the login page
    login_page.go_to_login_page()
    assert driver.current_url.startswith(LoginPage.LOGIN_URL), "Failed to navigate to Login Page"
    assert login_page.is_login_fields_visible(), "Login fields are not visible"

    # Step 2: Enter valid username
    email_entered = login_page.enter_email(email)
    assert email_entered, f"Email '{email}' was not entered correctly in the field"

    # Step 3: Enter valid password
    password_masked = login_page.enter_password(password)
    assert password_masked, "Password field is not masked or password was not entered correctly"

    # Step 4: Click on the Login button
    login_page.click_login()
    # Wait for redirect (explicit wait for dashboard element)
    for _ in range(10):
        if login_page.is_redirected_to_dashboard():
            break
        time.sleep(1)
    assert login_page.is_redirected_to_dashboard(), "User is not redirected to dashboard/home page after login"

    # Step 5: Verify user session is created
    session_created = login_page.is_session_token_created()
    assert session_created, "User session is not active or user details are not displayed"

    # Final assertion for complete flow using PageClass method
    assert login_page.login_with_valid_credentials(email, password), "End-to-end login_with_valid_credentials failed"
