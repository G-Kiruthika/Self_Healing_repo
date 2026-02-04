# test_login_invalid_password.py
# Selenium test for TC_LOGIN_003: Login with valid email and invalid password
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage
import time

# Test data for TC_LOGIN_003
test_email = "testuser@example.com"
test_invalid_password = "WrongPassword123"

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


def test_login_with_valid_email_invalid_password(driver):
    """
    TC_LOGIN_003: Attempt login with valid email and invalid password; verify error message and user remains on login page.
    Steps:
    1. Navigate to the login page
    2. Enter valid email address
    3. Enter incorrect password
    4. Click Login button
    5. Verify error message is displayed: 'Invalid email or password'
    6. Verify user remains on login page (not authenticated)
    """
    login_page = LoginPage(driver)
    login_page.go_to_login_page()

    # Step 1: Login page is displayed
    assert login_page.is_login_fields_visible(), "Login fields are not visible!"

    # Step 2: Enter valid email
    assert login_page.enter_email(test_email), f"Email '{test_email}' was not entered correctly!"

    # Step 3: Enter invalid password
    assert login_page.enter_password(test_invalid_password), "Password was not entered/masked correctly!"

    # Step 4: Click Login
    login_page.click_login()
    time.sleep(1)  # Wait for error message to appear

    # Step 5: Verify error message
    error_message = login_page.get_error_message()
    assert error_message is not None, "No error message displayed!"
    assert "invalid email or password" in error_message.lower(), f"Unexpected error message: {error_message}"

    # Step 6: Verify user remains on login page
    assert driver.current_url == login_page.LOGIN_URL, (
        f"User is not on login page after failed login! Current URL: {driver.current_url}"
    )

    # Traceability
    print("[TRACE] TC_LOGIN_003 executed: Login with valid email and invalid password.")
