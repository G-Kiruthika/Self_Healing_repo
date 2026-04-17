# test_tc_scrum74_008.py
"""
Test Case: TC_SCRUM74_008 - Forgot Password Workflow
Covers:
    1. Navigate to login page
    2. Click 'Forgot Password' link
    3. Validate navigation to password recovery page
    4. Validate presence of email input and submit button

Traceability:
- PageObjects: LoginPage, PasswordRecoveryPage
- Acceptance Criteria: AC_007
- Test Steps: See Jira TC_SCRUM74_008
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import time

from auto_scripts.Pages.LoginPage import LoginPage
from auto_scripts.Pages.PasswordRecoveryPage import PasswordRecoveryPage

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_tc_scrum74_008(driver):
    """
    TC_SCRUM74_008: End-to-end test for Forgot Password workflow.
    """
    login_page = LoginPage(driver)
    password_recovery_page = PasswordRecoveryPage(driver)

    # Step 1: Navigate to login page
    login_page.go_to_login_page()
    assert login_page.is_on_login_page(), "Login page is not displayed."

    # Step 2: Click on 'Forgot Password' link
    try:
        login_page.click_forgot_password()
    except TimeoutException:
        pytest.fail("'Forgot Password' link not found or not clickable.")

    # Step 3: Validate redirection to password recovery page
    try:
        password_recovery_page.wait.until(
            lambda d: d.current_url.startswith(password_recovery_page.PASSWORD_RECOVERY_URL)
        )
    except TimeoutException:
        # Fallback: Give time for navigation and check URL
        time.sleep(2)
    assert password_recovery_page.PASSWORD_RECOVERY_URL in driver.current_url, (
        f"Did not navigate to Password Recovery page. Current URL: {driver.current_url}"
    )

    # Step 4: Validate presence of email input and submit button
    assert password_recovery_page.verify_page_elements(), (
        "Email input and/or submit button not present on password recovery page."
    )

    print("TC_SCRUM74_008 passed: Forgot Password workflow navigation and UI validation successful.")
