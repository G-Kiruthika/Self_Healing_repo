# Test Script for TC-LOGIN-006: Forgot Password Link and Password Recovery Page
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import AssertionError
from auto_scripts.Pages.LoginPage import LoginPage
from auto_scripts.Pages.PasswordRecoveryPage import PasswordRecoveryPage

@pytest.fixture(scope='module')
def driver():
    options = Options()
    options.add_argument('--headless')  # Run in headless mode for CI/CD
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_tc_login_006_forgot_password_navigation_and_ui(driver):
    """
    Test Case TC-LOGIN-006
    1. Navigate to the login page
    2. Verify 'Forgot Password' link is visible and clickable
    3. Click on the 'Forgot Password' link
    4. Verify redirection to password recovery page
    5. Verify password recovery page displays email input field and instructions
    """
    login_page = LoginPage(driver)
    # Step 1 & 2: Navigate to login page and verify 'Forgot Password' link, then click it
    assert login_page.tc_login_006_verify_forgot_password_link_and_navigation(), (
        "Failed at LoginPage: Forgot Password link or navigation validation failed"
    )

    # Step 3: Verify Password Recovery Page UI
    recovery_page = PasswordRecoveryPage(driver)
    assert recovery_page.tc_login_006_verify_password_recovery_page_ui(), (
        "Failed at PasswordRecoveryPage: Email field or instructions missing"
    )

    # Additional assertions for traceability
    assert 'forgot-password' in driver.current_url, "Not on Password Recovery page URL after navigation"
    # Optionally, check instructions text if needed
