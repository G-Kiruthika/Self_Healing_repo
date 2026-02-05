# Test Script for TC-LOGIN-007: Username Recovery Flow
# Author: Enterprise Test Automation Agent
# This script validates the end-to-end username recovery flow using Selenium and the UsernameRecoveryPage PageClass.

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.UsernameRecoveryPage import UsernameRecoveryPage

TEST_EMAIL = 'user@example.com'  # Replace with valid test data if needed
LOGIN_URL = "https://ecommerce.example.com/login"
USERNAME_RECOVERY_URL = "https://ecommerce.example.com/forgot-username"

@pytest.fixture(scope='module')
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    # You may need to specify the path to chromedriver if not in PATH
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

@pytest.mark.tc_login_007
def test_tc_login_007_username_recovery_flow(driver):
    """
    Test Case TC-LOGIN-007:
    1. Navigate to the login page
    2. Click on 'Forgot Username' link
    3. Verify username recovery page is displayed
    Acceptance Criteria: TS-005
    """
    page = UsernameRecoveryPage(driver)

    # Step 1: Navigate to the login page
    page.navigate_to_login_page()
    assert LOGIN_URL in driver.current_url, f"Step 1 Failed: Expected URL '{LOGIN_URL}', got '{driver.current_url}'"
    # Verify 'Forgot Username' link is visible
    forgot_username_link = driver.find_element(*page.LOGIN_FORGOT_USERNAME_LINK)
    assert forgot_username_link.is_displayed(), "Step 1 Failed: 'Forgot Username' link is not visible"

    # Step 2: Click 'Forgot Username' link
    page.click_forgot_username_link()
    assert USERNAME_RECOVERY_URL in driver.current_url, f"Step 2 Failed: Expected to be redirected to '{USERNAME_RECOVERY_URL}', got '{driver.current_url}'"

    # Step 3: Verify username recovery page UI
    ui_valid = page.verify_username_recovery_page_ui()
    assert ui_valid, "Step 3 Failed: Username recovery page UI validation failed"

    # Optionally, test entering email and sending username
    entered = page.enter_email(TEST_EMAIL)
    assert entered, f"Failed to enter email '{TEST_EMAIL}' in the input field"
    page.click_send_username()
    # Check for success or error message
    success = page.is_success_message_displayed()
    error = page.is_error_message_displayed()
    assert success or error, "No success or error message displayed after submitting username recovery"
    if success:
        print("Username recovery succeeded: Success message displayed.")
    else:
        print("Username recovery failed: Error message displayed.")

    # Note: Email inbox verification is not implemented in PageClass
