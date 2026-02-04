# Selenium Test Script for TC_LOGIN_004: Login with Empty Email and Valid Password
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
from auto_scripts.Pages.LoginPage import LoginPage

# Test Data
LOGIN_URL = "https://app.example.com/login"
VALID_PASSWORD = "ValidPass123!"

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
    TC_LOGIN_004: Attempt login with empty email and valid password; verify validation error for email is displayed.
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
    assert driver.current_url == LOGIN_URL, "Login page did not load correctly."

    # Step 2: Leave email field empty (do not enter any email)
    assert login_page.enter_email("") is True, "Email field is not empty!"
    email_value = driver.find_element(*LoginPage.EMAIL_FIELD).get_attribute("value")
    assert email_value == "", "Email field is not empty after clearing."

    # Step 3: Enter valid password
    assert login_page.enter_password(VALID_PASSWORD), "Password was not entered/masked correctly!"
    password_field_type = driver.find_element(*LoginPage.PASSWORD_FIELD).get_attribute("type")
    assert password_field_type == "password", "Password field is not masked!"

    # Step 4: Click Login button
    login_page.click_login()
    time.sleep(1)  # Wait for validation error to appear

    # Step 5: Verify validation error 'Email is required' is displayed below email field
    try:
        validation_error = driver.find_element(*LoginPage.VALIDATION_ERROR)
        assert validation_error.is_displayed(), "Validation error not displayed!"
        assert "email is required" in validation_error.text.lower(), f"Unexpected validation error: {validation_error.text}"
    except NoSuchElementException:
        pytest.fail("Validation error element not found!")

    # Also verify user is still on login page
    assert driver.current_url == LOGIN_URL, "User is not on login page after failed login!"
