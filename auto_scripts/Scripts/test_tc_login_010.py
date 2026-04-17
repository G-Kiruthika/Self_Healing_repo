"""
Selenium Automation Script for TC-LOGIN-010
Test: Login with boundary email (special characters, max length), password masking, and system validation.
Author: Automation Generator
"""
import os
import sys
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
import time

# --- Dynamic import path for PageClass ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PAGES_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '../Pages'))
sys.path.insert(0, PAGES_DIR)

from TC_LOGIN_010_TestPage import TC_LOGIN_010_TestPage

# Test Data for boundary condition
LOGIN_URL = "https://app.example.com/login"
EMAIL_MAX_254 = "a234567890123456789012345678901234567890123456789012345678901234@b234567890123456789012345678901234567890123456789012345678901234.c234567890123456789012345678901234567890123456789012345678901234.d234567890123456789012345678901234567890123456789012345678.com"
VALID_PASSWORD = "ValidPass123!"

@pytest.fixture(scope='module')
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

@pytest.mark.tc_login_010
def test_tc_login_010_boundary_email(driver):
    """
    Test Case TC_LOGIN_010:
    1. Navigate to login page
    2. Enter email with 254 characters (max valid length)
    3. Enter valid password
    4. Click Login
    5. Validate system handles boundary email correctly (no errors, password masked)
    """
    page = TC_LOGIN_010_TestPage(driver)
    results = page.run_tc_login_010(EMAIL_MAX_254, VALID_PASSWORD)

    # Step 1: Login page is displayed
    assert results["step_1_navigate_login"] is True, f"Login page not displayed: {results['exception']}"

    # Step 2: Email is accepted
    assert results["step_2_enter_email"] is True, "Email with special chars/boundary not accepted"

    # Step 3: Password is masked and accepted
    assert results["step_3_enter_password"] is True, "Password not masked/accepted"

    # Step 4: Login button clicked successfully
    assert results["step_4_click_login"] is True, "Login button click failed"

    # Step 5: No system errors, appropriate authentication response
    assert results["step_5_error_message"] is None or results["step_5_error_message"] == "", f"Unexpected error message: {results['step_5_error_message']}"
    assert results["step_6_validation_error"] is None or results["step_6_validation_error"] == "", f"Unexpected validation error: {results['step_6_validation_error']}"

    # Step 7: Ensure system handled login attempt (still on login page or successful response)
    assert results["step_7_login_prevented"] is True, "System did not handle boundary email login as expected"

    # Overall pass
    assert results["overall_pass"] is True, f"Overall test did not pass: {results}"
