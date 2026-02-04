# Test Script for TC_LOGIN_013: Login with Maximum Allowed Password Length
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time

from auto_scripts.Pages.LoginPage import LoginPage

def generate_max_length_password(length=128):
    # Example: repeat a pattern to reach 128 characters
    pattern = "Aa1!"
    return (pattern * (length // len(pattern) + 1))[:length]

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

def test_login_with_max_length_password(driver):
    """
    TC_LOGIN_013: Attempt login with valid email and maximum allowed password length (128 characters).
    Steps:
    1. Navigate to the login page
    2. Enter valid email address
    3. Enter password at maximum allowed length (128 characters)
    4. Click on the Login button
    Acceptance Criteria: AC_007
    Expected:
        - Password is accepted and entered (no truncation)
        - Login attempt is processed (either success or error depending on credentials)
        - No validation error is shown for password length
    """
    login_page = LoginPage(driver)
    email = "testuser@example.com"
    max_length_password = generate_max_length_password()

    # Step 1: Navigate to the login page
    login_page.go_to_login_page()
    assert driver.current_url.startswith(LoginPage.LOGIN_URL), "Login page URL mismatch."

    # Step 2: Enter valid email address
    email_accepted = login_page.enter_email(email)
    assert email_accepted, f"Email '{email}' was not accepted in the email field."

    # Step 3: Enter password at maximum allowed length (128 characters)
    password_field = driver.find_element(*LoginPage.PASSWORD_FIELD)
    password_field.clear()
    password_field.send_keys(max_length_password)
    actual_value = password_field.get_attribute("value")
    assert len(actual_value) == 128, f"Password field did not accept 128 characters, got {len(actual_value)}."

    # Step 4: Click on the Login button
    login_page.click_login()
    time.sleep(1)  # Allow for page update

    # Accept both possible outcomes: login success or error, but no validation error for length
    validation_error_present = False
    try:
        validation_error = driver.find_element(*LoginPage.VALIDATION_ERROR)
        if validation_error.is_displayed() and "length" in validation_error.text.lower():
            validation_error_present = True
    except NoSuchElementException:
        pass
    assert not validation_error_present, "Validation error for password length was shown."

    # Accept success (dashboard) or login error
    login_success = login_page.is_redirected_to_dashboard()
    login_error = login_page.is_error_message_displayed()
    assert login_success or login_error, "Login attempt did not result in success or expected error."

    # Traceability
    print("TC_LOGIN_013 executed: Login with max length password. Email accepted:", email_accepted, "Password length:", len(actual_value), "Login success:", login_success, "Login error:", login_error)
