# test_tc_login_007_username_recovery.py
"""
Automated Selenium test for TC-LOGIN-007: Username Recovery Flow
Covers:
    1. Login page displays 'Forgot Username' link
    2. Clicking 'Forgot Username' redirects to Username Recovery page
    3. Username Recovery page displays correct fields and instructions
Traceability:
    - Uses LoginPage and UsernameRecoveryPage Page Objects
    - Test Case ID: 234 / TC-LOGIN-007
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage
from auto_scripts.Pages.UsernameRecoveryPage import UsernameRecoveryPage

# Test Data (could be parameterized or loaded from fixtures)
LOGIN_URL = "https://example-ecommerce.com/login"
USERNAME_RECOVERY_URL = "https://ecommerce.example.com/forgot-username"
REGISTERED_EMAIL = "testuser@example.com"  # Replace with valid test email if needed

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_tc_login_007_username_recovery_flow(driver):
    """
    TC-LOGIN-007: Username Recovery Flow
    Steps:
        1. Navigate to login page, verify 'Forgot Username' link is visible
        2. Click 'Forgot Username', verify redirect
        3. Verify username recovery page elements and instructions
    """
    # Step 1: Navigate to login page
    login_page = LoginPage(driver)
    login_page.load()
    assert login_page.is_displayed(), "Login page did not load successfully."
    # Verify 'Forgot Username' link is visible
    forgot_username_elem = driver.find_element(*LoginPage.FORGOT_USERNAME_LINK)
    assert forgot_username_elem.is_displayed(), "'Forgot Username' link not visible on login page."

    # Step 2: Click 'Forgot Username' and verify redirect
    forgot_username_elem.click()
    # Wait for URL to change
    from selenium.webdriver.support.ui import WebDriverWait
    WebDriverWait(driver, 10).until(lambda d: "forgot-username" in d.current_url)
    current_url = driver.current_url
    assert USERNAME_RECOVERY_URL in current_url, f"Did not redirect to username recovery page. Current URL: {current_url}"

    # Step 3: Verify username recovery page elements
    username_recovery_page = UsernameRecoveryPage(driver)
    assert username_recovery_page.is_loaded(), "Username recovery page did not load correctly."
    assert username_recovery_page.is_instructions_visible(), "Instructions are not visible on username recovery page."
    assert username_recovery_page.is_email_input_visible(), "Email input field is not visible."
    assert username_recovery_page.is_send_username_button_visible(), "Send Username button is not visible."
    # (Do not actually submit email for username, as test mailbox integration is not implemented)
