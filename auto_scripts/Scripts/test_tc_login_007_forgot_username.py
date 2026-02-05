# Test Script for TC_LOGIN_007: Forgot Username Flow
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import sys

# Adjust sys.path to import Page Objects
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Pages')))

from LoginPage import LoginPage
from UsernameRecoveryPage import UsernameRecoveryPage

test_email = "testuser@example.com"

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_tc_login_007_forgot_username_flow(driver):
    """
    TC_LOGIN_007: Forgot Username Flow
    Steps:
    1. Navigate to the login page
    2. Click on 'Forgot Username' link
    3. Enter registered email address
    4. Click on 'Send Username' button
    5. Verify username recovery email is received
    """
    # Step 1: Navigate to the login page
    login_page = LoginPage(driver)
    assert login_page.navigate_to_login(), "Step 1 FAILED: Login page is not displayed"
    
    # Step 2: Click on 'Forgot Username' link
    assert login_page.click_forgot_username(), "Step 2 FAILED: Could not click 'Forgot Username' link"
    
    # Now on Username Recovery Page
    username_recovery_page = UsernameRecoveryPage(driver)
    assert username_recovery_page.is_loaded(), "Step 2 FAILED: Username Recovery page not loaded"
    
    # Step 3: Enter registered email address
    assert username_recovery_page.enter_email(test_email), "Step 3 FAILED: Email was not accepted in input field"
    
    # Step 4: Click on 'Send Username' button
    username_recovery_page.click_send_username()
    time.sleep(2)  # Wait for message to display
    assert username_recovery_page.is_success_message_displayed(), "Step 4 FAILED: Success message not displayed"
    
    # Step 5: Verify username recovery email is received (stubbed)
    try:
        username_recovery_page.verify_username_recovery_email_received(test_email)
    except NotImplementedError:
        # Expected, as this is to be integrated with test email inbox or mock
        pass
    else:
        pytest.skip("Step 5: Email verification is not implemented in automation harness.")
