# Selenium Test Script for TC_LOGIN_002: Invalid Login Scenario
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from auto_scripts.Pages.LoginPage import LoginPage

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

def test_login_with_invalid_credentials(driver):
    """
    Test Case ID: TC_LOGIN_002
    Description: Attempt login with invalid email and valid password, verify error message and no authentication.
    Steps:
    1. Navigate to the login page
    2. Enter invalid email
    3. Enter valid password
    4. Click Login
    5. Verify error message and user is not redirected
    """
    login_page = LoginPage(driver)

    # Step 1: Go to login page
    login_page.go_to_login_page()
    assert login_page.is_login_fields_visible(), "Login fields should be visible on the login page."

    # Step 2: Enter invalid email
    email_entered = login_page.enter_email("invaliduser@example.com")
    assert email_entered, "Invalid email should be entered correctly."

    # Step 3: Enter valid password
    password_entered = login_page.enter_password("ValidPass123!")
    assert password_entered, "Password should be entered and masked."

    # Step 4: Click Login
    login_page.click_login()

    # Step 5: Verify error message and user is not redirected
    error_displayed = login_page.is_error_message_displayed("Invalid email or password")
    assert error_displayed, "Error message 'Invalid email or password' should be displayed."
    redirected = login_page.is_redirected_to_dashboard()
    assert not redirected, "User should not be redirected to dashboard after invalid login."

    # Negative session check
    session_created = login_page.is_session_token_created()
    assert not session_created, "Session token should NOT be created for invalid login."
