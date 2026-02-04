# Test Script for TC_LOGIN_006: Login with Empty Username Field
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import os
import sys

# Add Pages directory to sys.path for import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Pages')))
from LoginPage import LoginPage

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_login_empty_fields_validation(driver):
    """
    TC_LOGIN_006: Attempt login with empty username and valid password, expect validation error and remain on login page.
    Steps:
    1. Navigate to the login page [Test Data: URL: https://app.example.com/login]
    2. Leave username field empty
    3. Enter valid password [Test Data: Password: Test@1234]
    4. Click on the Login button
    5. Verify validation error is displayed: 'Username is required' or 'Please enter username', and user remains on login page and is not authenticated
    """
    login_page = LoginPage(driver)
    password = "Test@1234"
    # Step 1: Navigate to login page
    login_page.go_to_login_page()
    assert login_page.is_login_fields_visible(), "Login fields are not visible!"

    # Step 2: Leave username field empty
    email_field = driver.find_element(By.ID, "login-email")
    email_field.clear()
    assert email_field.get_attribute("value") == "", "Username field is not empty!"

    # Step 3: Enter valid password
    assert login_page.enter_password(password), "Password was not entered/masked correctly!"

    # Step 4: Click Login
    login_page.click_login()
    time.sleep(0.5)

    # Step 5: Validation error is displayed, user remains on login page, not authenticated
    validation_error = None
    try:
        validation_elem = driver.find_element(By.CSS_SELECTOR, ".invalid-feedback")
        if validation_elem.is_displayed():
            validation_error = validation_elem.text.strip()
    except NoSuchElementException:
        pass
    assert validation_error is not None, "Validation error message not displayed!"
    assert ("username is required" in validation_error.lower() or "please enter username" in validation_error.lower()), f"Expected username required validation, got: {validation_error}"
    assert driver.current_url == LoginPage.LOGIN_URL, "User is not on login page after empty username attempt!"
    # Ensure user is not authenticated (no session token)
    cookies = driver.get_cookies()
    session_token = next((cookie for cookie in cookies if 'session' in cookie['name'].lower()), None)
    assert session_token is None, "Session token should not be created when username is empty!"
