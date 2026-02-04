# Selenium Test Script for TC_LOGIN_011: Login with maximum length email
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope='function')
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_with_max_length_email(driver):
    """
    TC_LOGIN_011: Login with email address of maximum valid length (254 characters) and valid password.
    Steps:
    1. Navigate to the login page
    2. Enter email address with 254 characters
    3. Enter valid password
    4. Click on the Login button
    5. Assert email is accepted and displayed, password is masked, and login is processed (success if registered, error if not)
    """
    # Arrange
    login_page = LoginPage(driver)
    max_length_email = (
        "a123456789012345678901234567890123456789012345678901234567890123@"
        "b123456789012345678901234567890123456789012345678901234567890123."
        "c123456789012345678901234567890123456789012345678901234567890123."
        "d123456789012345678901234567890123456789012345678.com"
    )
    valid_password = "ValidPass123!"

    # Act
    login_page.go_to_login_page()
    assert driver.current_url.startswith(LoginPage.LOGIN_URL), "Login page URL mismatch."
    assert login_page.is_login_fields_visible(), "Login fields are not visible."

    email_accepted = login_page.enter_email(max_length_email)
    assert email_accepted, f"Email of max length was not accepted or not entered correctly. Entered: {max_length_email}"

    password_masked = login_page.enter_password(valid_password)
    assert password_masked, "Password input is not masked (type != 'password')."

    login_page.click_login()
    time.sleep(2)  # Wait for login processing

    # Accept both possible outcomes: login success or error
    login_success = login_page.is_redirected_to_dashboard()
    login_error = login_page.is_error_message_displayed()

    assert login_success or login_error, (
        "Neither login success nor expected error message was detected after submitting max length email."
    )
    if login_success:
        assert login_page.is_session_token_created(), "Session token was not created after login success."
    else:
        assert login_error, "Expected error message not displayed for invalid login."
