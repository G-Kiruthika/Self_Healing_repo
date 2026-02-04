# Test script for TC_LOGIN_003: Invalid login credentials
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
import time
import os
import sys

# Ensure Pages directory is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../Pages')))
from LoginPage import LoginPage

@pytest.fixture(scope="module")
def driver():
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

def test_login_invalid_credentials(driver):
    """
    TC_LOGIN_003: Attempt login with invalid username and valid password, expect error and stay on login page.
    Steps:
    1. Navigate to the login page
    2. Enter invalid username
    3. Enter valid password
    4. Click Login button
    5. Verify error message is displayed: 'Invalid username or password' and user remains on login page
    """
    login_page = LoginPage(driver)
    invalid_email = "invaliduser@example.com"
    valid_password = "Test@1234"
    
    # 1. Navigate to the login page
    login_page.go_to_login_page()
    assert login_page.is_login_fields_visible(), "Login fields are not visible!"
    
    # 2. Enter invalid username
    assert login_page.enter_email(invalid_email), "Invalid username was not entered correctly!"
    
    # 3. Enter valid password
    assert login_page.enter_password(valid_password), "Password was not entered/masked correctly!"
    
    # 4. Click Login button
    login_page.click_login()
    time.sleep(1)  # Wait for error message
    
    # 5. Verify error message is displayed and user remains on login page
    error_message = login_page.get_error_message()
    assert error_message is not None, "Error message not displayed for invalid credentials!"
    assert "invalid username or password" in error_message.lower(), f"Expected error message 'Invalid username or password', got: {error_message}"
    assert driver.current_url == login_page.LOGIN_URL, "User did not remain on the login page after invalid login!"
