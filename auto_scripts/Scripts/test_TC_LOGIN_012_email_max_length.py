# Test Script for TC_LOGIN_012: Email Exceeding Max Length
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time

from auto_scripts.Pages.LoginPage import LoginPage

def generate_long_email():
    # Generates an email string longer than 255 characters
    local = 'a' * 64
    domain1 = 'b' * 63
    domain2 = 'c' * 63
    domain3 = 'd' * 63
    email = f"{local}@{domain1}.{domain2}.{domain3}.comextra"  # >255 chars
    return email

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_email_exceeding_max_length(driver):
    """
    TC_LOGIN_012: Attempt to enter email address exceeding maximum length (255+ characters)
    Steps:
    1. Navigate to the login page
    2. Attempt to enter email address exceeding maximum length (255+ characters)
    3. Click on the Login button
    Acceptance Criteria: Email field either truncates input or shows validation error
    Expected: Error message displayed: 'Email exceeds maximum length' or input is truncated
    """
    login_page = LoginPage(driver)
    long_email = generate_long_email()
    password = "testpassword"

    # Step 1: Navigate to login page
    login_page.go_to_login_page()
    assert driver.current_url == LoginPage.LOGIN_URL, "Login page did not load."
    assert login_page.is_login_fields_visible(), "Login fields are not visible."

    # Step 2 & 3: Enter long email and check for truncation or error
    email_field = driver.find_element(*LoginPage.EMAIL_FIELD)
    email_field.clear()
    email_field.send_keys(long_email)
    actual_value = email_field.get_attribute("value")
    # If the field truncates input, actual_value will be shorter than input
    input_truncated = len(actual_value) < len(long_email)
    login_page.enter_password(password)
    login_page.click_login()
    time.sleep(1)
    # Check for validation error message
    validation_error = ""
    try:
        error_elements = driver.find_elements(*LoginPage.VALIDATION_ERROR)
        for el in error_elements:
            if el.is_displayed() and ("maximum length" in el.text.lower() or "exceeds" in el.text.lower()):
                validation_error = el.text
                break
    except NoSuchElementException:
        pass
    error_displayed = validation_error != ""
    assert input_truncated or error_displayed, (
        f"Neither truncation nor error message was detected. Actual value: {actual_value}, Validation error: {validation_error}")
    if error_displayed:
        print(f"Validation error displayed: {validation_error}")
    elif input_truncated:
        print(f"Input was truncated to: {actual_value} (length: {len(actual_value)})")
