# Selenium test script for TC_LOGIN_011: Login with maximum length email
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage
import time

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')  # Run headless for CI
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_with_max_length_email(driver):
    """
    TC_LOGIN_011: Login with email address of maximum valid length (254 characters) and valid password.
    Steps:
    1. Navigate to the login page
    2. Enter email address with 254 characters
    3. Enter valid password
    4. Click on the Login button
    5. Assert email is accepted and displayed, password is masked, and login is processed (success if registered, error if not)
    Acceptance Criteria: SCRUM-91
    """
    # Test Data
    max_length_email = (
        "a123456789012345678901234567890123456789012345678901234567890123@"
        "b123456789012345678901234567890123456789012345678901234567890123."
        "c123456789012345678901234567890123456789012345678901234567890123."
        "d123456789012345678901234567890123456789012345.com"
    )
    valid_password = "ValidPass123!"

    login_page = LoginPage(driver)
    login_page.go_to_login_page()

    # Step 1: Assert login page is displayed
    assert login_page.is_login_fields_visible(), "Login fields are not visible on the login page."
    assert driver.current_url.startswith(LoginPage.LOGIN_URL), f"Unexpected URL: {driver.current_url}"

    # Step 2 & 3: Enter max length email and valid password
    email_accepted = login_page.enter_email(max_length_email)
    assert email_accepted, "Max length email was not accepted or displayed correctly."
    password_masked = login_page.enter_password(valid_password)
    assert password_masked, "Password input is not masked (type != 'password')."

    # Step 4: Click Login
    login_page.click_login()
    time.sleep(2)  # Wait for login response (adjust as needed for app speed)

    # Step 5: Accept both possible outcomes: login success or error
    login_success = login_page.is_redirected_to_dashboard()
    login_error = login_page.is_error_message_displayed()
    assert login_success or login_error, (
        "Neither successful login nor error message displayed after submitting max length email."
    )
    if login_success:
        print("Login succeeded with max length email (user is registered).")
    else:
        print("Login failed as expected with error message (user not registered or invalid credentials).")
