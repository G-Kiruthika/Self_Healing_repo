'''
Test Script for TC_LOGIN_007: Username Recovery Workflow
Author: Automation Generator
Description: End-to-end Selenium test for username recovery using PageClass orchestration.
'''
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.TC_LOGIN_007_TestPage import TC_LOGIN_007_TestPage

@pytest.fixture(scope='module')
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_tc_login_007_username_recovery(driver):
    """
    Test Case: TC_LOGIN_007 - Username Recovery Workflow
    Steps:
      1. Navigate to login page
      2. Click 'Forgot Username'
      3. Enter registered email
      4. Click 'Send Username'
      5. Validate success message
      6. Check email inbox (mocked)
    """
    email = 'testuser@example.com'
    test_page = TC_LOGIN_007_TestPage(driver)
    results = test_page.run_tc_login_007(email)

    # Step 1: Login page displayed
    assert results['step_1_navigate_login'] is True, f"Login page not displayed: {results.get('exception')}"
    # Step 2: Click 'Forgot Username' successful
    assert results['step_2_click_forgot_username'] is True, f"Failed to click 'Forgot Username': {results.get('exception')}"
    # Step 3: Email entered successfully
    assert results['step_3_enter_email'] is True, f"Failed to enter email: {results.get('exception')}"
    # Step 4: Click 'Send Username' successful
    assert results['step_4_click_send_username'] is True, f"Failed to submit username recovery: {results.get('exception')}"
    # Step 5: Success message validation
    assert results['step_5_success_message'] is not None, f"No success message: {results.get('exception')}"
    expected_msg = 'Username sent to your email'
    assert expected_msg.lower() in results['step_5_success_message'].lower(), \
        f"Expected success message '{expected_msg}' not found. Got: {results['step_5_success_message']}"
    # Step 6: Email inbox check (mocked)
    assert results['step_6_email_inbox_check'] is not None, f"Email inbox check failed: {results.get('exception')}"
    assert email in results['step_6_email_inbox_check'], \
        f"Username recovery email not received for {email}. Got: {results['step_6_email_inbox_check']}"
    # Overall pass
    assert results['overall_pass'] is True, f"Test failed at one or more steps: {results}"
