# test_TC_SCRUM74_008_password_recovery.py
"""
Test Script for TC_SCRUM74_008: End-to-End Password Recovery Flow

- Navigates to login page
- Clicks 'Forgot Password' link
- Verifies password recovery page elements
- Enters registered email
- Submits the form
- Validates success message
- Checks (mocked) email inbox for reset link

Author: Automation Pipeline
"""
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from auto_scripts.Pages.PasswordRecoveryPage import PasswordRecoveryPage

# Test Data
LOGIN_URL = "https://app.example.com/login"
REGISTERED_EMAIL = "testuser@example.com"
FORGOT_PASSWORD_LINK = (By.LINK_TEXT, "Forgot Password")

@pytest.fixture(scope="module")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

@pytest.mark.tc_scrum74_008
def test_tc_scrum74_008_password_recovery(driver):
    """
    Test Case TC_SCRUM74_008: Password Recovery Workflow
    """
    wait = WebDriverWait(driver, 10)

    # Step 1: Navigate to login page
    driver.get(LOGIN_URL)
    try:
        forgot_link = wait.until(EC.visibility_of_element_located(FORGOT_PASSWORD_LINK))
    except TimeoutException:
        pytest.fail("Forgot Password link not found on login page.")
    assert forgot_link.is_displayed(), "Forgot Password link should be visible."

    # Step 2: Click on 'Forgot Password' link
    forgot_link.click()
    # Expect redirection to password recovery page
    recovery_page = PasswordRecoveryPage(driver)
    try:
        wait.until(EC.visibility_of_element_located(PasswordRecoveryPage.EMAIL_INPUT))
    except TimeoutException:
        pytest.fail("Email input not found on password recovery page after navigation.")
    assert driver.current_url.startswith("https://app.example.com/forgot-password"), \
        f"Expected password recovery URL, got {driver.current_url}"

    # Step 3: Verify password recovery page elements
    assert recovery_page.verify_page_elements() is True, "Page elements verification failed."

    # Step 4: Enter registered email address
    recovery_page.enter_email(REGISTERED_EMAIL)

    # Step 5: Click Submit button
    recovery_page.click_submit()

    # Step 6: Validate success message
    success_msg = recovery_page.get_success_message()
    assert success_msg is not None, "Success message not displayed after submitting recovery request."
    assert "email has been sent" in success_msg.lower(), f"Unexpected success message: {success_msg}"

    # Step 7: Check (mocked) email inbox for password reset link
    reset_link = recovery_page.mock_check_email_inbox_for_reset_link(REGISTERED_EMAIL)
    assert reset_link.startswith("https://app.example.com/reset-password"), \
        f"Reset link format invalid: {reset_link}"

    # Traceability output (for CI/CD logs)
    print("TC_SCRUM74_008 results:", {
        "success_message": success_msg,
        "reset_link": reset_link
    })
