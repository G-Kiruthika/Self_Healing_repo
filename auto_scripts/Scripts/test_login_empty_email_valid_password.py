# Test Script for TC_LOGIN_004: Login with Empty Email and Valid Password
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import sys
import os

# Adjust the import path if running in CI/CD or different folder structure
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Pages')))
from LoginPage import LoginPage

@pytest.fixture(scope='function')
def driver():
    options = Options()
    options.add_argument('--headless')  # Remove if you want to see the browser
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_with_empty_email_and_valid_password(driver):
    """
    TC_LOGIN_004: Attempt login with empty email and valid password, expect 'Email is required' validation error.
    Steps:
    1. Navigate to the login page
    2. Leave email field empty
    3. Enter valid password
    4. Click on the Login button
    5. Assert validation error 'Email is required' is displayed below email field and login is prevented
    """
    login_page = LoginPage(driver)
    # Step 1: Navigate to login page
    login_page.go_to_login_page()
    assert driver.current_url == LoginPage.LOGIN_URL, "Login page URL mismatch"
    assert login_page.is_login_fields_visible(), "Login fields are not visible"

    # Step 2: Leave email field empty
    email_entered = login_page.enter_email("")
    assert email_entered, "Email field is not empty as expected"

    # Step 3: Enter valid password
    password = "ValidPass123!"  # Use valid test password
    password_masked = login_page.enter_password(password)
    assert password_masked, "Password field is not masked or not entered correctly"

    # Step 4: Click on the Login button
    login_page.click_login()

    # Step 5: Assert validation error 'Email is required' is displayed and login is prevented
    try:
        validation_error = driver.find_element(*LoginPage.VALIDATION_ERROR)
        error_text = validation_error.text if validation_error.is_displayed() else ""
    except NoSuchElementException:
        error_text = ""
    assert "Email is required" in error_text, f"Expected validation error 'Email is required', got: '{error_text}'"
    assert driver.current_url == LoginPage.LOGIN_URL, "User was redirected away from login page; login should be prevented"
    # Optionally: check that dashboard header is not visible
    assert not login_page.is_redirected_to_dashboard(), "User should not be redirected to dashboard after invalid login"
