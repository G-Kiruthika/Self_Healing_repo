# Test Script for TC_LOGIN_010: Password Recovery End-to-End
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time

from auto_scripts.Pages.LoginPage import LoginPage
from auto_scripts.Pages.PasswordRecoveryPage import PasswordRecoveryPage

# Test Data
REGISTERED_EMAIL = "testuser@example.com"
LOGIN_URL = "https://app.example.com/login"
PASSWORD_RECOVERY_URL = "https://app.example.com/password-recovery"

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_tc_login_010_password_recovery_flow(driver):
    """
    TC_LOGIN_010: End-to-end test for password recovery flow.
    Steps:
        1. Navigate to the password recovery page via Forgot Password link
        2. Enter registered email address
        3. Click on the Submit button
        4. Check email inbox for password reset link (stub)
    Acceptance Criteria: SCRUM-91
    """
    # Step 1: Navigate to login page and click 'Forgot Password' link
    login_page = LoginPage(driver)
    login_page.go_to_login_page()
    assert login_page.is_forgot_password_link_visible(), "Forgot Password link should be visible on login page"
    assert login_page.click_forgot_password_link(), "Should be able to click Forgot Password link"
    time.sleep(2)  # Wait for redirect
    assert driver.current_url.startswith(PASSWORD_RECOVERY_URL), f"Should be redirected to password recovery page, got {driver.current_url}"

    # Step 2: Enter registered email address
    recovery_page = PasswordRecoveryPage(driver)
    assert recovery_page.is_email_input_visible(), "Email input should be visible on password recovery page"
    assert recovery_page.enter_email(REGISTERED_EMAIL), f"Should be able to enter email: {REGISTERED_EMAIL}"

    # Step 3: Click Submit and check for success message
    assert recovery_page.is_submit_button_visible(), "Submit button should be visible on password recovery page"
    recovery_page.submit_recovery()
    time.sleep(2)  # Wait for response
    assert recovery_page.is_success_message_displayed(), "Success message should be displayed after submitting recovery"

    # Step 4: (Stub) Check email inbox for reset link
    # This is a stub and should be implemented with an email API/service
    result = recovery_page.check_email_inbox_for_reset_link(REGISTERED_EMAIL)
    assert result is NotImplemented, "Email inbox check is a stub and should return NotImplemented"
