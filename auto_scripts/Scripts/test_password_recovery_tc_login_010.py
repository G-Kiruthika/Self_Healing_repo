# test_password_recovery_tc_login_010.py
"""
Test Script for TC_LOGIN_010: Password Recovery End-to-End

Test Case ID: 132
Description: Test password recovery workflow via Forgot Password link.
Steps:
  1. Navigate to the password recovery page via Forgot Password link
  2. Enter registered email address
  3. Click on the Submit button
  4. Check email inbox for password reset link
Expected Results:
  1. Password recovery page is displayed
  2. Email is entered in the field
  3. Success message 'Password reset link has been sent to your email' is displayed
  4. Password reset email is received with valid reset link

Traceability:
  - Acceptance Criteria: SCRUM-91
  - PageClass: PasswordRecoveryPage
"""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.PasswordRecoveryPage import PasswordRecoveryPage

TEST_EMAIL = "testuser@example.com"
EXPECTED_SUCCESS_MSG = "Password reset link has been sent to your email"
RECOVERY_URL = "https://app.example.com/forgot-password"

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


def test_tc_login_010_password_recovery(driver):
    """
    End-to-end test for password recovery (TC_LOGIN_010)
    """
    page = PasswordRecoveryPage(driver)
    results = page.run_tc_login_010(TEST_EMAIL)

    # Step 1: Navigated to recovery page
    assert results["step_1_navigate_recovery"], "Failed to navigate to password recovery page."
    assert RECOVERY_URL in driver.current_url, f"Did not land on expected URL: {RECOVERY_URL}"

    # Step 2: Email entered
    assert results["step_2_enter_email"], "Failed to enter email in the field."

    # Step 3: Submit clicked
    assert results["step_3_click_submit"], "Failed to click Submit button."

    # Step 4: Success message
    assert results["step_4_success_message"], (
        f"Expected success message not found. Got: {results['step_4_success_message']}"
    )
    assert EXPECTED_SUCCESS_MSG.lower() in results["step_4_success_message"].lower(), (
        f"Success message mismatch. Expected: '{EXPECTED_SUCCESS_MSG}', Got: '{results['step_4_success_message']}'"
    )

    # Step 5: Email inbox check (mocked)
    reset_link = results["step_5_email_inbox_check"]
    assert reset_link is not None, "No reset link found in mocked inbox."
    assert reset_link.startswith("https://app.example.com/reset-password?token="), (
        f"Reset link format invalid: {reset_link}"
    )

    # Overall pass
    assert results["overall_pass"], f"Test failed. Details: {results}"
    assert results["exception"] is None, f"Exception occurred: {results['exception']}"
