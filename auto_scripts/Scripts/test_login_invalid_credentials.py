# Test Script for TC_LOGIN_003: Invalid Login Credentials
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage
import time

@pytest.fixture(scope='function')
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_with_invalid_credentials(driver):
    """
    TC_LOGIN_003: Attempt login with invalid username and valid password;
    verify error message and user remains on login page.
    Steps:
        1. Navigate to the login page
        2. Enter invalid username
        3. Enter valid password
        4. Click Login button
        5. Verify error message is displayed: 'Invalid username or password'
        6. Verify user remains on login page (not authenticated)
    """
    # Test Data
    invalid_email = 'invaliduser@example.com'
    valid_password = 'Test@1234'
    login_page = LoginPage(driver)

    # Step 1: Navigate to the login page
    login_page.go_to_login_page()
    assert driver.current_url == LoginPage.LOGIN_URL, "Login page URL mismatch!"
    assert login_page.is_login_fields_visible(), "Login fields are not visible!"

    # Step 2: Enter invalid username
    assert login_page.enter_email(invalid_email), "Invalid username was not entered correctly!"

    # Step 3: Enter valid password
    assert login_page.enter_password(valid_password), "Password was not entered/masked correctly!"

    # Step 4: Click Login button
    login_page.click_login()
    time.sleep(1)  # Wait for error message

    # Step 5: Verify error message is displayed
    error_message = login_page.get_error_message()
    assert error_message is not None, "No error message displayed!"
    assert "invalid username or password" in error_message.lower(), f"Unexpected error message: {error_message}"

    # Step 6: Verify user remains on login page (not authenticated)
    assert driver.current_url == LoginPage.LOGIN_URL, "User is not on login page after failed login!"
