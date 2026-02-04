# Test Script for TC_LOGIN_003: Invalid Login Credentials
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage
import time

@pytest.fixture(scope='module')
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_tc_login_003_invalid_credentials(driver):
    """
    TC_LOGIN_003: Attempt login with invalid username and valid password, expect error and stay on login page.
    Steps:
        1. Navigate to the login page [Test Data: URL: https://app.example.com/login]
        2. Enter invalid username [Test Data: Username: invaliduser@example.com]
        3. Enter valid password [Test Data: Password: Test@1234]
        4. Click on the Login button
        5. Verify error message is displayed: 'Invalid username or password' and user remains on login page
    """
    login_page = LoginPage(driver)
    invalid_email = "invaliduser@example.com"
    valid_password = "Test@1234"

    # Step 1: Navigate to the login page
    login_page.go_to_login_page()
    assert login_page.is_login_fields_visible(), "Login fields are not visible!"

    # Step 2: Enter invalid username
    assert login_page.enter_email(invalid_email), "Invalid username was not entered correctly!"

    # Step 3: Enter valid password
    assert login_page.enter_password(valid_password), "Password was not entered/masked correctly!"

    # Step 4: Click on the Login button
    login_page.click_login()
    time.sleep(1)  # Wait for error message to appear

    # Step 5: Verify error message and user remains on login page
    error_message = login_page.get_error_message()
    assert error_message is not None, "Error message not displayed for invalid credentials!"
    assert "invalid username or password" in error_message.lower(), f"Expected error message 'Invalid username or password', got: {error_message}"
    assert driver.current_url == login_page.LOGIN_URL, "User did not remain on the login page after invalid login!"
