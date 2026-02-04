# Selenium Test Script for TC_LOGIN_004: Login with empty email and valid password
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope='module')
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_with_empty_email_and_valid_password(driver):
    """
    TC_LOGIN_004: Attempt login with empty email and valid password; verify validation error for missing email.
    Steps:
        1. Navigate to the login page
        2. Leave email field empty
        3. Enter valid password
        4. Click Login button
        5. Verify validation error 'Email is required' is displayed below email field
    Acceptance Criteria: SCRUM-91
    """
    # Test Data
    valid_password = "ValidPass123!"
    login_page = LoginPage(driver)

    # Step 1: Navigate to the login page
    login_page.go_to_login_page()
    assert login_page.is_login_fields_visible(), "Login fields are not visible!"
    assert driver.current_url == LoginPage.LOGIN_URL, f"Expected URL {LoginPage.LOGIN_URL}, got {driver.current_url}"

    # Step 2: Leave email field empty
    email_field = driver.find_element(*LoginPage.EMAIL_FIELD)
    email_field.clear()
    assert email_field.get_attribute("value") == "", "Email field is not empty!"

    # Step 3: Enter valid password
    assert login_page.enter_password(valid_password), "Password was not entered/masked correctly!"

    # Step 4: Click Login button
    login_page.click_login()
    time.sleep(0.5)  # Wait for validation message

    # Step 5: Verify validation error 'Email is required' is displayed below email field
    try:
        validation_errors = driver.find_elements(*LoginPage.VALIDATION_ERROR)
        found = False
        for err in validation_errors:
            if err.is_displayed() and "email is required" in err.text.strip().lower():
                found = True
                break
        assert found, "Validation error 'Email is required' not displayed below email field!"
    except NoSuchElementException:
        # Fallback: check for any generic error message
        error_message = login_page.get_error_message()
        assert error_message and "email is required" in error_message.lower(), (
            f"Validation error 'Email is required' not displayed! Error message: {error_message}"
        )
