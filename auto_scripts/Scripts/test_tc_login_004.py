import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
import os
import sys
import time

# Add Pages directory to sys.path for import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../Pages')))
from TC_LOGIN_004_TestPage import TC_LOGIN_004_TestPage

@pytest.fixture(scope='module')
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_tc_login_004(driver):
    """
    Test Case TC-LOGIN-004: Negative login - Empty email, valid password.
    Steps:
      1. Navigate to login page
      2. Leave email field empty
      3. Enter valid password
      4. Click Login
      5. Assert validation error is shown
      6. Assert user remains on login page
    """
    # Test Data
    valid_password = 'ValidPass123!'
    url = 'https://ecommerce.example.com/login'
    # Instantiate the PageClass
    page = TC_LOGIN_004_TestPage(driver)
    results = page.run_tc_login_004(valid_password, url)

    # Step 1: Navigate to login page
    assert results['step_1_navigate_login'] is True, f"Step 1 failed: {results.get('exception','')}"
    # Step 2: Leave email field empty
    assert results['step_2_leave_email_empty'] is True, "Step 2 failed: Email field not left empty."
    # Step 3: Enter valid password
    assert results['step_3_enter_password'] is True, "Step 3 failed: Password not entered."
    # Step 4: Click Login button
    assert results['step_4_click_login'] is True, "Step 4 failed: Login button not clicked."
    # Step 5: Validate error is displayed
    assert results['step_5_validation_error'] is not None and len(results['step_5_validation_error']) > 0, \
        "Step 5 failed: Validation error message not displayed."
    # Step 6: Validate login is prevented (still on login page)
    assert results['step_6_login_prevented'] is True, "Step 6 failed: User navigated away from login page."
    # Overall pass
    assert results['overall_pass'] is True, f"Overall test failed: {results.get('exception','')}"
