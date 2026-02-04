# Test script for TC_LOGIN_007: Validate login with both username and password fields left empty
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import os
import sys

# Ensure the Pages directory is in sys.path for import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../Pages')))
from LoginPage import LoginPage

@pytest.fixture(scope='function')
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_empty_fields_validation(driver):
    """
    TC_LOGIN_007: Validate login with both username and password fields left empty.
    Steps:
    1. Navigate to the login page
    2. Leave username field empty
    3. Leave password field empty
    4. Click on the Login button
    5. Verify validation errors are displayed: 'Username is required' and 'Password is required'.
    6. Verify login is not processed, user remains on login page and is not authenticated.
    """
    login_page = LoginPage(driver)
    login_page.go_to_login_page()

    # Step 1: Login page is displayed with empty username and password fields
    assert login_page.is_login_fields_visible(), "Login fields are not visible!"
    email_field = driver.find_element(By.ID, "login-email")
    password_field = driver.find_element(By.ID, "login-password")
    assert email_field.get_attribute("value") == "", "Username field is not empty!"
    assert password_field.get_attribute("value") == "", "Password field is not empty!"

    # Step 2 & 3: Leave both fields empty (already empty)
    email_field.clear()
    password_field.clear()
    assert email_field.get_attribute("value") == "", "Username field is not empty after clear!"
    assert password_field.get_attribute("value") == "", "Password field is not empty after clear!"

    # Step 4: Click on the Login button
    driver.find_element(By.ID, "login-submit").click()
    time.sleep(0.5)  # Wait for validation error to appear

    # Step 5: Verify validation errors are displayed
    validation_errors = []
    try:
        error_elems = driver.find_elements(By.CSS_SELECTOR, ".invalid-feedback")
        for elem in error_elems:
            if elem.is_displayed():
                validation_errors.append(elem.text.strip())
    except NoSuchElementException:
        pass
    assert any("username is required" in err.lower() for err in validation_errors), \
        f"Validation error for empty username not found! Errors: {validation_errors}"
    assert any("password is required" in err.lower() for err in validation_errors), \
        f"Validation error for empty password not found! Errors: {validation_errors}"

    # Step 6: Verify login is not processed, user remains on login page and is not authenticated
    assert driver.current_url == LoginPage.LOGIN_URL, "User is not on login page after empty field validation!"
    cookies = driver.get_cookies()
    session_token = next((cookie for cookie in cookies if 'session' in cookie['name'].lower()), None)
    assert session_token is None, "Session token should not be created for empty fields!"
    try:
        user_icon = driver.find_element(By.CSS_SELECTOR, ".user-profile-name")
        assert not user_icon.is_displayed(), "User profile icon should not be displayed for unauthenticated user!"
    except Exception:
        pass
