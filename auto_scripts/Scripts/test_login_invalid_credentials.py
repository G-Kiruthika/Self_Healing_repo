# Test Script for TC_SCRUM74_003: Invalid Login Credentials
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_with_nonexistent_email_and_any_password(driver):
    """
    Test Case: TC_SCRUM74_003
    Steps:
    1. Navigate to the login page
    2. Enter non-existent email (nonexistent@example.com)
    3. Enter any password (AnyPass123!)
    4. Click on the Login button
    Acceptance Criteria: Login fails with error message 'Invalid credentials'
    """
    login_page = LoginPage(driver)

    # Step 1: Navigate to login page
    assert login_page.navigate_to_login(), "Login page did not load correctly (email/password fields not visible)"

    # Step 2: Enter non-existent email
    email = "nonexistent@example.com"
    assert login_page.enter_nonexistent_email(email), f"Email '{email}' was not accepted in the field"

    # Step 3: Enter any password
    password = "AnyPass123!"
    assert login_page.enter_any_password(password), "Password field did not accept input or was not masked"

    # Step 4: Click Login and verify error message
    assert login_page.click_login_and_verify_invalid_credentials(), "Expected error message 'Invalid credentials' not displayed after login attempt"
