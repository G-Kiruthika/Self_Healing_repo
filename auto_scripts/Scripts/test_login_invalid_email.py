# Selenium Test Script for TC_LOGIN_002: Login with Invalid Email
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage
import time

@pytest.fixture(scope='module')
def driver():
    # Configure Chrome options for headless execution and reliability
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_with_invalid_email(driver):
    """
    TC_LOGIN_002: Attempt login with invalid email and valid password; verify error message and user remains on login page.
    Steps:
    1. Navigate to the login page
    2. Enter invalid email address
    3. Enter valid password
    4. Click Login button
    5. Verify error message is displayed: 'Invalid email or password'
    6. Verify user remains on login page (not authenticated)
    """
    # Test Data
    login_url = "https://app.example.com/login"
    invalid_email = "invaliduser@example.com"
    valid_password = "ValidPass123!"

    login_page = LoginPage(driver)

    # Step 1: Navigate to the login page
    login_page.go_to_login_page()
    assert driver.current_url == login_url, f"Expected URL: {login_url}, but got: {driver.current_url}"

    # Step 2: Enter invalid email address
    assert login_page.is_login_fields_visible(), "Login fields are not visible!"
    assert login_page.enter_email(invalid_email), f"Invalid email '{invalid_email}' was not entered correctly!"

    # Step 3: Enter valid password
    assert login_page.enter_password(valid_password), "Password was not entered/masked correctly!"

    # Step 4: Click Login button
    login_page.click_login()
    time.sleep(1)  # Wait for error message to appear

    # Step 5: Verify error message is displayed
    error_message = login_page.get_error_message()
    assert error_message is not None, "No error message displayed!"
    assert "invalid email or password" in error_message.lower(), f"Unexpected error message: {error_message}"

    # Step 6: Verify user remains on login page (not authenticated)
    assert driver.current_url == login_url, "User is not on login page after failed login!"
