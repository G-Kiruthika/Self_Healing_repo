# Test Script for TC_LOGIN_005: Login with valid email and empty password
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from auto_scripts.Pages.LoginPage import LoginPage
import time

@pytest.fixture(scope='function')
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_login_with_valid_email_and_empty_password(driver):
    """
    Test Case ID: TC_LOGIN_005
    Description: Attempt login with valid email and empty password; verify validation error for password is displayed.
    Steps:
        1. Navigate to the login page
        2. Enter valid email address (testuser@example.com)
        3. Leave password field empty
        4. Click Login button
        5. Verify validation error 'Password is required' is displayed below password field
    Acceptance Criteria: SCRUM-91
    """
    login_page = LoginPage(driver)
    valid_email = "testuser@example.com"
    # Step 1: Navigate to the login page
    login_page.go_to_login_page()
    assert login_page.is_login_fields_visible(), "Login fields are not visible!"

    # Step 2: Enter valid email address
    assert login_page.enter_email(valid_email), f"Email '{valid_email}' was not entered correctly!"

    # Step 3: Leave password field empty (do not enter anything)
    password_field = driver.find_element(*LoginPage.PASSWORD_FIELD)
    password_field.clear()
    assert password_field.get_attribute("value") == "", "Password field is not empty!"

    # Step 4: Click Login button
    login_page.click_login()
    time.sleep(1)  # Wait for validation error to appear

    # Step 5: Verify validation error for password is displayed
    try:
        validation_error = driver.find_element(*LoginPage.VALIDATION_ERROR)
        assert validation_error.is_displayed(), "Validation error not displayed!"
        assert "password is required" in validation_error.text.lower(), f"Unexpected validation error: {validation_error.text}"
    except NoSuchElementException:
        pytest.fail("Validation error element not found!")
