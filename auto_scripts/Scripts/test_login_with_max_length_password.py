# Test Script for TC_LOGIN_013: Login with valid email and password at maximum allowed length (128 characters)
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from auto_scripts.Pages.LoginPage import LoginPage
import time

# Test Data for TC_LOGIN_013
test_email = "testuser@example.com"
test_password = "Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!Aa1!"

@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_with_max_length_password(driver):
    """
    TC_LOGIN_013: Login with valid email and password at maximum allowed length (128 characters).
    Steps:
    1. Navigate to the login page [Test Data: URL: https://app.example.com/login]
    2. Enter valid email address [Test Data: Email: testuser@example.com]
    3. Enter password at maximum allowed length (128 characters)
    4. Click on the Login button
    Expected: Password is accepted and entered, login attempt is processed without validation error.
    Acceptance Criteria: AC_007
    """
    login_page = LoginPage(driver)

    # Step 1: Navigate to login page
    login_page.go_to_login_page()
    assert driver.current_url.startswith(LoginPage.LOGIN_URL), "Login page URL mismatch."
    assert login_page.is_login_fields_visible(), "Login fields are not visible."

    # Step 2: Enter valid email address
    email_accepted = login_page.enter_email(test_email)
    assert email_accepted, f"Email '{test_email}' was not accepted in the email field."

    # Step 3: Enter password at maximum allowed length (128 characters)
    password_masked = login_page.enter_password(test_password)
    assert password_masked, "Password field did not mask input as expected."
    assert len(test_password) == 128, f"Test password length is not 128 characters: {len(test_password)}"

    # Step 4: Click on the Login button
    login_page.click_login()
    time.sleep(2)  # Wait for login attempt to process

    # Expected: Login is processed without validation error
    # Accept both possible outcomes: login success or error (but no validation error)
    try:
        validation_error_present = False
        validation_error_elements = driver.find_elements_by_css_selector('.invalid-feedback')
        for el in validation_error_elements:
            if el.is_displayed():
                validation_error_present = True
                break
        assert not validation_error_present, "Validation error was displayed on login with max-length password."
    except WebDriverException:
        # If selector is missing, treat as no validation error
        pass

    login_success = login_page.is_redirected_to_dashboard()
    login_error = login_page.is_error_message_displayed()
    assert login_success or login_error, (
        "Login attempt did not result in success or error message. "
        "Expected either dashboard redirection or error message display."
    )
