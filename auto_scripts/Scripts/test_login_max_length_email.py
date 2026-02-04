# Test Script for TC_LOGIN_011: Login with Maximum Length Email
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
import time
import string
import random

from auto_scripts.Pages.LoginPage import LoginPage

def generate_max_length_email():
    # 254 characters
    # Example: a123...@b123...c123...d123...com (already provided in test data)
    return (
        "a123456789012345678901234567890123456789012345678901234567890123"
        "@b123456789012345678901234567890123456789012345678901234567890123."
        "c123456789012345678901234567890123456789012345678901234567890123."
        "d123456789012345678901234567890123456789012345.com"
    )

def get_valid_password():
    return "ValidPass123!"

@pytest.fixture(scope='module')
def driver():
    # Update this to your desired browser and driver path
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_with_max_length_email_and_valid_password(driver):
    """
    TC_LOGIN_011: Attempt login with an email address of maximum allowed length (254 characters) and a valid password.
    Steps:
    1. Navigate to the login page
    2. Enter email address with 254 characters
    3. Enter valid password
    4. Click on the Login button
    5. Assert that the email is accepted and displayed
    6. Assert that the password is masked and entered
    7. Assert system processes the login attempt appropriately (success if registered, error if not)
    """
    login_page = LoginPage(driver)
    max_length_email = generate_max_length_email()
    valid_password = get_valid_password()

    # Step 1: Navigate to login page
    login_page.go_to_login_page()
    assert driver.current_url.startswith(LoginPage.LOGIN_URL), "Login page URL mismatch."
    assert login_page.is_login_fields_visible(), "Login fields not visible."

    # Step 2: Enter max-length email and validate it's accepted
    email_accepted = login_page.enter_email(max_length_email)
    actual_email = driver.find_element(*LoginPage.EMAIL_FIELD).get_attribute("value")
    assert email_accepted, "Email was not accepted by the input field."
    assert len(actual_email) == 254, f"Email input length is {len(actual_email)}, expected 254."
    assert actual_email == max_length_email, "Actual email in field does not match input."

    # Step 3: Enter valid password and check masking
    password_masked = login_page.enter_password(valid_password)
    actual_password_type = driver.find_element(*LoginPage.PASSWORD_FIELD).get_attribute("type")
    assert password_masked, "Password was not accepted as masked input."
    assert actual_password_type == "password", f"Password input type is {actual_password_type}, expected 'password'."

    # Step 4: Click Login
    login_page.click_login()
    time.sleep(2)  # Wait for possible redirect or error

    # Step 5: System response
    login_success = login_page.is_redirected_to_dashboard()
    login_error = login_page.is_error_message_displayed()

    # At least one should be True: either success or error (if not registered)
    assert login_success or login_error, (
        "Neither dashboard loaded nor error message displayed after login attempt with max-length email."
    )

    # Traceability output
    print("Test Results for TC_LOGIN_011:")
    print(f"- Email accepted: {email_accepted}")
    print(f"- Email length OK: {len(actual_email) == 254}")
    print(f"- Password masked: {password_masked}")
    print(f"- Login success: {login_success}")
    print(f"- Login error displayed: {login_error}")
