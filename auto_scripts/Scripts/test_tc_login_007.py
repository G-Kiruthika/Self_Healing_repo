# test_tc_login_007.py
"""
Automated Test Script for TC_LOGIN_007: Username Recovery Flow
Covers:
  1. Navigate to login page
  2. Click 'Forgot Username' link
  3. Enter registered email address
  4. Click 'Send Username'
  5. Verify success message and (optionally) email receipt

PageObjects used:
  - LoginPage (auto_scripts/Pages/LoginPage.py)
  - UsernameRecoveryPage (auto_scripts/Pages/UsernameRecoveryPage.py)

Test Data:
  - Login URL: https://example-ecommerce.com/login
  - Registered Email: testuser@example.com
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from auto_scripts.Pages.LoginPage import LoginPage
from auto_scripts.Pages.UsernameRecoveryPage import UsernameRecoveryPage

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_tc_login_007_username_recovery_flow(driver):
    """
    TC_LOGIN_007: End-to-end test for username recovery via login page.
    """
    LOGIN_URL = "https://example-ecommerce.com/login"
    REGISTERED_EMAIL = "testuser@example.com"

    # Step 1: Navigate to login page
    login_page = LoginPage(driver)
    assert login_page.navigate_to_login(), "Step 1 Failed: Login page did not load."
    assert login_page.is_login_page_displayed(), "Step 1 Failed: Login page elements not visible."

    # Step 2: Click 'Forgot Username' link
    assert login_page.click_forgot_username(), "Step 2 Failed: Could not click 'Forgot Username' link."

    # Step 3: UsernameRecoveryPage loaded
    username_recovery_page = UsernameRecoveryPage(driver)
    assert username_recovery_page.is_loaded(), "Step 3 Failed: Username recovery page did not load."
    assert username_recovery_page.is_email_input_visible(), "Step 3 Failed: Email input not visible."
    assert username_recovery_page.is_send_username_button_visible(), "Step 3 Failed: 'Send Username' button not visible."

    # Step 4: Enter registered email and click 'Send Username'
    assert username_recovery_page.enter_email(REGISTERED_EMAIL), "Step 4 Failed: Email input failed."
    username_recovery_page.click_send_username()

    # Step 5: Verify success message displayed
    assert username_recovery_page.is_success_message_displayed(), (
        "Step 5 Failed: Success message not displayed or incorrect."
    )

    # Optional: Step 6 - Verify email received (NotImplemented)
    # try:
    #     assert username_recovery_page.verify_username_recovery_email_received(REGISTERED_EMAIL), (
    #         "Step 6 Failed: Username recovery email not received."
    #     )
    # except NotImplementedError:
    #     pytest.skip("Email verification is not implemented in this test harness.")
