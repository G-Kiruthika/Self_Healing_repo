import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.TC_LOGIN_003_TestPage import TC_LOGIN_003_TestPage
import time

# Test Data (ideally this would be parameterized or loaded from fixtures)
LOGIN_URL = "https://ecommerce.example.com/login"
VALID_EMAIL = "testuser@example.com"
INVALID_PASSWORD = "WrongPassword456"
EXPECTED_ERROR_MESSAGE = "Invalid email or password"

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')  # Comment this line if you want to see the browser
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_tc_login_003_negative_login_and_username_recovery(driver):
    """
    TC-LOGIN-003: Negative login with valid email and wrong password, plus username recovery flow.
    1. Navigate to login page
    2. Enter valid email
    3. Enter wrong password
    4. Click Login
    5. Assert error message
    6. Assert still on login page
    7. Trigger 'Forgot Username' and recover username
    """
    # Instantiate test page object
    tc_login_003 = TC_LOGIN_003_TestPage(driver)

    # Step 1: Navigate to login page
    driver.get(LOGIN_URL)
    time.sleep(1)  # Let page load
    assert tc_login_003.login_page.is_on_login_page(), "Login page is not displayed after navigation."

    # Step 2: Enter valid email
    tc_login_003.login_page.enter_email(VALID_EMAIL)
    # Optionally, assert email field value (not always accessible due to masking)

    # Step 3: Enter incorrect password
    tc_login_003.login_page.enter_password(INVALID_PASSWORD)
    # Optionally, assert password masking (not directly testable)

    # Step 4: Click Login
    tc_login_003.login_page.click_login()

    # Step 5: Validate error message
    error_message = tc_login_003.login_page.get_error_message()
    assert error_message is not None, "Expected error message not displayed."
    assert EXPECTED_ERROR_MESSAGE.lower() in error_message.lower(), (
        f"Unexpected error message: {error_message}")

    # Step 6: Verify user remains on login page
    assert tc_login_003.login_page.is_on_login_page(), (
        "User is not on login page after failed login.")

    # Step 7: Click 'Forgot Username' link
    tc_login_003.login_page.click_forgot_username()

    # Step 8: Recover username
    tc_login_003.username_recovery_page.enter_email(VALID_EMAIL)
    tc_login_003.username_recovery_page.submit_recovery()
    confirmation = tc_login_003.username_recovery_page.get_confirmation_message()
    assert confirmation is not None, "Username recovery confirmation message not displayed."
    assert "username" in confirmation.lower() or "sent" in confirmation.lower(), (
        f"Unexpected confirmation message: {confirmation}")
