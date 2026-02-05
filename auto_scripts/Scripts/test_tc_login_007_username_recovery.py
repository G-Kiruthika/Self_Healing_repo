# Selenium Test Script for TC-LOGIN-007: Username Recovery Flow
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.UsernameRecoveryPage import UsernameRecoveryPage

# Test Data
LOGIN_PAGE_URL = "https://ecommerce.example.com/login"
USERNAME_RECOVERY_URL = "https://ecommerce.example.com/forgot-username"
VALID_EMAIL = "testuser@example.com"  # Replace with a valid test email address

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

@pytest.fixture
def username_recovery_page(driver):
    return UsernameRecoveryPage(driver)

def test_tc_login_007_username_recovery_flow(username_recovery_page):
    """
    Test Case ID: TC-LOGIN-007
    Description: Username Recovery Flow
    Steps:
      1. Navigate to the login page
      2. Click on the 'Forgot Username' link
      3. Verify username recovery page is displayed
    """
    # Step 1: Navigate to the login page
    username_recovery_page.navigate_to_login_page()
    assert username_recovery_page.driver.current_url.startswith(LOGIN_PAGE_URL), (
        f"[Step 1] Expected to be on {LOGIN_PAGE_URL}, but got {username_recovery_page.driver.current_url}"
    )
    forgot_username_elements = username_recovery_page.driver.find_elements(*UsernameRecoveryPage.LOGIN_FORGOT_USERNAME_LINK)
    assert forgot_username_elements and forgot_username_elements[0].is_displayed(), (
        "[Step 1] 'Forgot Username' link is not visible on the login page."
    )

    # Step 2: Click on 'Forgot Username' link
    username_recovery_page.click_forgot_username_link()
    assert username_recovery_page.driver.current_url.startswith(USERNAME_RECOVERY_URL), (
        f"[Step 2] Expected to be on {USERNAME_RECOVERY_URL}, but got {username_recovery_page.driver.current_url}"
    )

    # Step 3: Verify username recovery page is displayed
    assert username_recovery_page.verify_username_recovery_page_ui(), (
        "[Step 3] Username recovery page UI validation failed. Input fields or instructions missing."
    )

    # Optional: Negative scenario, check error message when invalid email is used (not required by TC-LOGIN-007)
    # username_recovery_page.enter_email("invalid_email")
    # username_recovery_page.click_send_username()
    # assert username_recovery_page.is_error_message_displayed(), "Error message not displayed for invalid email."

    # Optional: Positive scenario, check success message (requires valid test email and backend integration)
    # username_recovery_page.enter_email(VALID_EMAIL)
    # username_recovery_page.click_send_username()
    # assert username_recovery_page.is_success_message_displayed(), "Success message not displayed after valid email submission."
