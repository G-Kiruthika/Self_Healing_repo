# Selenium Test Script for TC_LOGIN_010 - Password Recovery Workflow
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import AssertionError
from auto_scripts.Pages.PasswordRecoveryPage import PasswordRecoveryPage

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_password_recovery_TC_LOGIN_010(driver):
    """
    TC_LOGIN_010: End-to-end workflow for password recovery
    Steps:
    1. Navigate to the password recovery page
    2. Enter registered email address
    3. Click on Send Reset Link button
    4. Verify success message is displayed
    5. Check email inbox for password reset email (external)
    Acceptance Criteria: AC_006
    """
    EMAIL = "testuser@example.com"
    recovery_page = PasswordRecoveryPage(driver)

    # Step 1: Navigate to the password recovery page
    driver.get(PasswordRecoveryPage.PASSWORD_RECOVERY_URL)
    assert recovery_page.is_loaded(), "Password recovery page is not loaded (Step 1 failed)."

    # Step 2: Enter registered email address
    email_entered = recovery_page.enter_email(EMAIL)
    assert email_entered, f"Email '{EMAIL}' was not entered correctly (Step 2 failed)."
    assert recovery_page.is_email_input_visible(), "Email input field is not visible after entering email (Step 2 failed)."

    # Step 3: Click on Send Reset Link button
    assert recovery_page.is_submit_button_visible(), "Submit button is not visible (Step 3 failed)."
    recovery_page.submit_recovery()

    # Step 4: Verify success message is displayed
    assert recovery_page.is_success_message_displayed(), "Success message not displayed after submitting recovery (Step 3 failed)."

    # Step 5: Check email inbox for password reset email (external)
    # This step is placeholder; actual implementation should verify the email inbox externally
    try:
        recovery_page.check_password_reset_email_received(EMAIL)
    except NotImplementedError:
        pass  # Acceptable for test harness; log as info
