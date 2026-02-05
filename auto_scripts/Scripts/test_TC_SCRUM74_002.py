# Selenium Test Script for TC_SCRUM74_002
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
from auto_scripts.Pages.LoginPage import LoginPage

test_data = {
    "url": "https://app.example.com/login",
    "invalid_email": "invalidemail@",
    "valid_password": "ValidPass123!",
    "expected_email_error": "Enter a valid email address",
    "expected_login_error": "Invalid email or username"
}

@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_TC_SCRUM74_002_invalid_email_login(driver):
    """
    Test Case: TC_SCRUM74_002
    Steps:
      1. Navigate to the login page
      2. Enter invalid email format
      3. Enter valid password
      4. Click on the Login button
      5. Assert error messages
    """
    login_page = LoginPage(driver)

    # Step 1: Navigate to the login page
    assert login_page.navigate_to_login(), "Login page is not displayed"

    # Step 2: Enter invalid email format
    assert login_page.enter_invalid_email_format(test_data["invalid_email"]), "Invalid email not entered correctly"
    # Wait for validation error to appear if any
    time.sleep(0.5)
    email_error_msg = login_page.get_email_format_error_message()
    assert email_error_msg is not None, "No email format error message displayed"
    # Optionally check for specific error text if available
    # assert test_data["expected_email_error"] in email_error_msg

    # Step 3: Enter valid password
    assert login_page.enter_valid_password_for_invalid_email(test_data["valid_password"]), "Password not accepted or not masked"

    # Step 4: Click on the Login button
    login_failed = login_page.click_login_for_invalid_email()
    assert login_failed, "Login did not fail as expected for invalid email format"

    # Step 5: Assert error message 'Invalid email or username' is displayed
    error_displayed = login_page.is_error_message_displayed(test_data["expected_login_error"])
    assert error_displayed, f"Expected login error message '{test_data['expected_login_error']}' not displayed"

    # Step 6: Ensure user remains on login page
    on_login_page = driver.current_url.startswith(test_data["url"])
    assert on_login_page, "User did not remain on login page after failed login"
