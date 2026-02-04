# Test Script for TC_LOGIN_003: Login with valid email and invalid password
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import AssertionError
import time
import os
import sys

# Ensure Pages directory is in sys.path for import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../Pages')))
from LoginPage import LoginPage

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_TC_LOGIN_003_valid_email_invalid_password(driver):
    """
    TC_LOGIN_003: Attempt login with valid email and invalid password; verify error message and user remains on login page.
    Steps:
    1. Navigate to the login page
    2. Enter valid email address
    3. Enter incorrect password
    4. Click Login button
    5. Verify error message is displayed: 'Invalid email or password'
    6. Verify user remains on login page (not authenticated)
    """
    login_page = LoginPage(driver)
    VALID_EMAIL = "testuser@example.com"
    INVALID_PASSWORD = "WrongPassword123"

    # Step 1: Navigate to login page
    login_page.go_to_login_page()
    assert login_page.is_login_fields_visible(), "Login fields are not visible!"
    
    # Step 2: Enter valid email address
    assert login_page.enter_email(VALID_EMAIL), "Email was not entered correctly!"
    
    # Step 3: Enter invalid password
    assert login_page.enter_password(INVALID_PASSWORD), "Password was not entered/masked correctly!"
    
    # Step 4: Click Login button
    login_page.click_login()
    time.sleep(1)  # Wait for error message to appear
    
    # Step 5: Verify error message is displayed
    error_message = login_page.get_error_message()
    assert error_message is not None, "No error message displayed!"
    assert "invalid email or password" in error_message.lower(), f"Unexpected error message: {error_message}"
    
    # Step 6: Verify user remains on login page
    assert driver.current_url == login_page.LOGIN_URL, "User is not on login page after failed login!"
    
    # Optionally, ensure user is not authenticated (no session token, profile icon not visible)
    cookies = driver.get_cookies()
    session_token = next((cookie for cookie in cookies if 'session' in cookie['name'].lower()), None)
    assert session_token is None, "Session token should not be created for failed login!"
