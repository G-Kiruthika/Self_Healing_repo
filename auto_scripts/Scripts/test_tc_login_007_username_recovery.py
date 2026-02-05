# Test Script for TC-LOGIN-007: Username Recovery Flow
# Location: auto_scripts/Scripts/test_tc_login_007_username_recovery.py
# Traceability: TestCaseId=234, Acceptance Criteria=TS-005

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import AssertionError
from auto_scripts.Pages.UsernameRecoveryPage import UsernameRecoveryPage

# Test Data
LOGIN_PAGE_URL = "https://ecommerce.example.com/login"
USERNAME_RECOVERY_URL = "https://ecommerce.example.com/forgot-username"
VALID_EMAIL = "testuser@example.com"  # Replace with valid email for environment

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

@pytest.mark.tc_login_007
@pytest.mark.parametrize("email", [VALID_EMAIL])
def test_tc_login_007_username_recovery_flow(driver, email):
    """
    Test Case TC-LOGIN-007: Username Recovery Flow
    Steps:
      1. Navigate to the login page
      2. Click on 'Forgot Username' link
      3. Verify username recovery page is displayed
    Acceptance Criteria: TS-005
    """
    page = UsernameRecoveryPage(driver)

    # Step 1: Navigate to the login page
    page.navigate_to_login_page()
    assert LOGIN_PAGE_URL in driver.current_url, (
        f"[TC-LOGIN-007][Step 1] Failed: Not on Login Page. Current URL: {driver.current_url}")
    assert driver.find_element(*page.LOGIN_FORGOT_USERNAME_LINK).is_displayed(), (
        "[TC-LOGIN-007][Step 1] Failed: 'Forgot Username' link not visible.")

    # Step 2: Click 'Forgot Username' link
    page.click_forgot_username_link()
    assert USERNAME_RECOVERY_URL in driver.current_url, (
        f"[TC-LOGIN-007][Step 2] Failed: Not redirected to Username Recovery Page. Current URL: {driver.current_url}")

    # Step 3: Verify username recovery page UI
    assert page.verify_username_recovery_page_ui(), (
        "[TC-LOGIN-007][Step 3] Failed: Username Recovery Page UI validation failed.")

    # Traceability assertion for reporting
    print("[TC-LOGIN-007] Username Recovery Page flow validated successfully.")
