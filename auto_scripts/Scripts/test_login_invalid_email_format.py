# Test Script for TC_LOGIN_020: Login with Invalid Email Format
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage
import time

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_invalid_email_format(driver):
    """
    TC_LOGIN_020: Validate error when logging in with an invalid email format (missing @ symbol).
    Steps:
    1. Navigate to the login page
    2. Enter email in invalid format (missing @ symbol)
    3. Enter valid password
    4. Click on the Login button
    5. Validate error 'Please enter a valid email address' is displayed
    """
    login_page = LoginPage(driver)
    invalid_email = "testuserexample.com"  # missing @
    valid_password = "ValidPass123!"
    expected_error = "Please enter a valid email address"

    # Step 1: Navigate to the login page
    login_page.go_to_login_page()
    assert login_page.is_login_fields_visible(), "Login fields are not visible!"

    # Step 2: Enter email in invalid format
    assert login_page.enter_email(invalid_email), "Invalid email was not entered correctly!"

    # Step 3: Enter valid password
    assert login_page.enter_password(valid_password), "Password was not entered/masked correctly!"

    # Step 4: Click on the Login button
    login_page.click_login()
    time.sleep(1)  # Wait for validation error message

    # Step 5: Validate error message
    error_message = login_page.get_validation_error_message()
    assert error_message is not None, "No validation error message displayed!"
    assert expected_error in error_message, f"Expected error '{expected_error}' not found in '{error_message}'"
