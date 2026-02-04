# Test Script for TC_LOGIN_020: Invalid email format validation on LoginPage
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
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_invalid_email_format(driver):
    """
    TC_LOGIN_020: Attempt login with invalid email format (missing '@'), expect validation error.
    Steps:
    1. Navigate to the login page
    2. Enter email in invalid format
    3. Enter valid password
    4. Click on the Login button
    5. Verify validation error 'Please enter a valid email address' is displayed
    """
    login_page = LoginPage(driver)
    invalid_email = "testuserexample.com"  # missing '@'
    valid_password = "ValidPass123!"
    # Use the PageClass workflow for this negative scenario
    validation_error = login_page.login_invalid_email_format(invalid_email, valid_password)
    assert validation_error is not None, "Validation error message was not displayed!"
    assert "valid email address" in validation_error.lower(), f"Unexpected validation error: {validation_error}"
    print(f"Validation error displayed: {validation_error}")
