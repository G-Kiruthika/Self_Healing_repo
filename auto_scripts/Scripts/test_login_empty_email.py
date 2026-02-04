# test_login_empty_email.py
# Test Script for TC_LOGIN_004: Login with empty email and valid password
# Generated automatically from PageClass LoginPage
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage

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

def test_login_with_empty_email_and_valid_password(driver):
    """
    Test Case ID: TC_LOGIN_004
    Description: Attempt login with empty email and valid password, verify validation error.
    Steps:
        1. Navigate to the login page
        2. Leave email field empty
        3. Enter valid password
        4. Click Login button
        5. Verify validation error 'Email is required' is displayed below email field
    Acceptance Criteria: SCRUM-91
    """
    login_page = LoginPage(driver)
    # Step 1: Navigate to the login page
    login_page.go_to_login_page()
    assert driver.current_url == LoginPage.LOGIN_URL, "Login page did not load as expected."
    assert login_page.is_login_fields_visible(), "Login fields are not visible."
    # Step 2: Leave email field empty (do nothing)
    # Step 3: Enter valid password
    valid_password = "ValidPass123!"  # Test data as per test case
    password_masked = login_page.enter_password(valid_password)
    assert password_masked, "Password field is not masked or could not enter password."
    # Step 4: Click Login button
    login_page.click_login()
    # Step 5: Verify validation error 'Email is required' is displayed below email field
    validation_error_displayed = login_page.login_with_empty_email_and_valid_password(valid_password)
    assert validation_error_displayed, "Validation error 'Email is required' was not displayed as expected."
