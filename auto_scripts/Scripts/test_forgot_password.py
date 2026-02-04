# test_forgot_password.py
# Selenium automation test for TC_LOGIN_010: Forgot Password workflow
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time

from auto_scripts.Pages.LoginPage import LoginPage
from auto_scripts.Pages.PasswordRecoveryPage import PasswordRecoveryPage

test_email = "testuser@example.com"
login_url = "https://app.example.com/login"

@pytest.fixture(scope="module")
def driver():
    # Headless Chrome for CI environments; adjust as needed
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_forgot_password_workflow(driver):
    """
    TC_LOGIN_010: Forgot Password End-to-End Flow
    1. Navigate to login page and click 'Forgot Password'
    2. Enter registered email address
    3. Submit recovery request
    4. Assert success message is displayed
    5. (External) Check email inbox for password reset link
    """
    # Step 1: Go to login page and initiate Forgot Password
    login_page = LoginPage(driver)
    login_page.go_to_login_page()
    assert login_page.is_forgot_password_link_visible(), "Forgot Password link should be visible on login page."
    clicked = login_page.click_forgot_password_link()
    assert clicked, "Failed to click 'Forgot Password' link."
    # Allow time for navigation
    time.sleep(2)

    # Step 2: On Password Recovery Page, enter email
    recovery_page = PasswordRecoveryPage(driver)
    assert recovery_page.is_loaded(), "Password Recovery page did not load."
    assert recovery_page.is_email_input_visible(), "Email input field is not visible."
    email_entered = recovery_page.enter_email(test_email)
    assert email_entered, f"Failed to enter email: {test_email}"

    # Step 3: Submit recovery
    assert recovery_page.is_submit_button_visible(), "Submit button is not visible."
    recovery_page.submit_recovery()
    # Allow time for response
    time.sleep(2)

    # Step 4: Assert success message is displayed
    assert recovery_page.is_success_message_displayed(), \
        "Success message not displayed after submitting password recovery."

    # Step 5: (External) Check email inbox for password reset link
    # This is a placeholder; actual implementation depends on test harness/external service
    try:
        recovery_page.check_password_reset_email_received(test_email)
    except NotImplementedError:
        pytest.skip("Email inbox check for password reset link is not implemented in test environment.")
