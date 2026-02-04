# Test Script for TC_LOGIN_004: Login with valid username and invalid password
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage

# Test Data for TC_LOGIN_004
LOGIN_URL = "https://app.example.com/login"
VALID_USERNAME = "testuser@example.com"
INVALID_PASSWORD = "WrongPass@123"

@pytest.fixture(scope='module')
def driver():
    # Setup Chrome WebDriver (headless for CI)
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_valid_username_invalid_password(driver):
    """
    TC_LOGIN_004: Attempt login with valid username and invalid password, expect error and remain on login page.
    Steps:
    1. Navigate to the login page
    2. Enter valid username
    3. Enter invalid password
    4. Click on the Login button
    5. Verify error message is displayed: 'Invalid username or password' and user remains on login page
    """
    login_page = LoginPage(driver)

    # Step 1: Navigate to login page
    login_page.go_to_login_page()
    assert driver.current_url == LOGIN_URL, f"Did not navigate to login page. Current URL: {driver.current_url}"
    assert login_page.is_login_fields_visible(), "Login fields are not visible!"

    # Step 2: Enter valid username
    assert login_page.enter_email(VALID_USERNAME), "Valid username was not entered correctly!"

    # Step 3: Enter invalid password
    assert login_page.enter_password(INVALID_PASSWORD), "Invalid password was not entered/masked correctly!"

    # Step 4: Click Login
    login_page.click_login()

    # Step 5: Verify error message and user remains on login page
    import time
    time.sleep(1)  # Wait for error message to appear
    error_message = login_page.get_error_message()
    assert error_message is not None, "Error message not displayed for invalid credentials!"
    assert "invalid username or password" in error_message.lower(), \
        f"Expected error message 'Invalid username or password', got: {error_message}"
    assert driver.current_url == LOGIN_URL, "User did not remain on the login page after invalid login!"
