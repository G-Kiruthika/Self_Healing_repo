# Test Script for TC_LOGIN_007: Empty Fields Validation (Login)
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

def test_TC_LOGIN_007_empty_fields_validation(driver):
    """
    Test Case ID: 161
    Test Case: TC_LOGIN_007 - Empty Fields Validation
    1. Navigate to the login page
    2. Leave username field empty
    3. Leave password field empty
    4. Click on the Login button
    5. Verify login is not processed and validation errors are displayed: 'Username is required' and 'Password is required'
    """
    login_page = LoginPage(driver)
    login_page.go_to_login_page()

    # Step 1: Login page is displayed with empty username and password fields
    assert login_page.is_login_fields_visible(), "Login fields are not visible!"
    email_field = driver.find_element(*LoginPage.EMAIL_FIELD)
    password_field = driver.find_element(*LoginPage.PASSWORD_FIELD)
    assert email_field.get_attribute("value") == "", "Username field is not empty!"
    assert password_field.get_attribute("value") == "", "Password field is not empty!"

    # Step 2 & 3: Leave both fields empty (already empty)
    # Step 4: Click on the Login button
    login_page.click_login()
    time.sleep(1)  # Wait for validation errors

    # Step 4: Validation errors are displayed: 'Username is required' and 'Password is required'
    validation_errors = driver.find_elements(*LoginPage.VALIDATION_ERROR)
    assert validation_errors, "No validation errors found!"
    found_username_error = False
    found_password_error = False
    for error_elem in validation_errors:
        if error_elem.is_displayed():
            error_text = error_elem.text.lower()
            if "username is required" in error_text or "email is required" in error_text:
                found_username_error = True
            if "password is required" in error_text:
                found_password_error = True
    assert found_username_error, "Username required validation error not displayed!"
    assert found_password_error, "Password required validation error not displayed!"

    # Step 5: Verify login is not processed (user remains on login page and not authenticated)
    assert driver.current_url == LoginPage.LOGIN_URL, "User is not on login page after empty fields validation!"
    # Optionally, check that user profile/dashboard is NOT visible
    assert not login_page.is_redirected_to_dashboard(), "User should not be redirected to dashboard!"
