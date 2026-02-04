# Test Script for TC_LOGIN_002: Login with invalid email and valid password
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage
import time

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

def test_login_invalid_email_valid_password(driver):
    """
    TC_LOGIN_002: Attempt login with invalid email and valid password; verify error message and user remains on login page.
    Steps:
    1. Navigate to the login page [Test Data: URL: https://app.example.com/login]
    2. Enter invalid email address [Test Data: Email: invaliduser@example.com]
    3. Enter valid password [Test Data: Password: ValidPass123!]
    4. Click on the Login button
    5. Verify error message displayed: 'Invalid email or password'
    6. Verify user remains on login page (not authenticated)
    """
    login_page = LoginPage(driver)
    login_page.go_to_login_page()
    assert login_page.is_login_fields_visible(), "Login fields are not visible!"
    assert login_page.enter_email("invaliduser@example.com"), "Invalid email was not entered correctly!"
    assert login_page.enter_password("ValidPass123!"), "Password was not entered/masked correctly!"
    login_page.click_login()
    time.sleep(1)  # Wait for error message
    error_message = login_page.get_error_message()
    assert error_message is not None, "No error message displayed!"
    assert "invalid email or password" in error_message.lower(), f"Unexpected error message: {error_message}"
    assert driver.current_url == login_page.LOGIN_URL, "User is not on login page after failed login!"
