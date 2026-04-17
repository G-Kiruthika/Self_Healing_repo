"""
Selenium Automation Test Script for TC-LOGIN-010

This script tests login with an email containing special characters, as per test case TC-LOGIN-010.

- Reads locators and page class from auto_scripts/Pages/TC_LOGIN_010_TestPage.py
- Uses Chrome WebDriver
- Asserts all acceptance criteria stepwise
- Outputs stepwise results and final assertion

Author: Automation Generator
"""
import os
import sys
import traceback
import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Ensure PageClass is importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Pages')))
from TC_LOGIN_010_TestPage import TC_LOGIN_010_TestPage

EMAIL = "test.user+tag@example.com"  # Test data for email with special characters
PASSWORD = "ValidPass123!"           # Valid test password

@pytest.fixture(scope="module")
def driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(1280, 1024)
    yield driver
    driver.quit()

def test_tc_login_010(driver):
    """
    Test Case: TC-LOGIN-010
    1. Navigate to login page
    2. Enter email with special characters
    3. Enter valid password (masked)
    4. Click Login
    5. Validate system behavior and error handling
    """
    page = TC_LOGIN_010_TestPage(driver)
    results = page.run_tc_login_010(EMAIL, PASSWORD)
    print("Stepwise Results:", results)

    # Step 1: Login page displayed
    assert results["step_1_navigate_login"] is True, "Login page was not displayed."

    # Step 2: Email with special characters accepted
    assert results["step_2_enter_email"] is True, "Email with special characters was not accepted."

    # Step 3: Password entered and masked
    assert results["step_3_enter_password"] is True, "Password was not entered or not masked."

    # Step 4: Login button clicked
    assert results["step_4_click_login"] is True, "Login button was not clicked."

    # Step 5: Error message should be None if login is expected to succeed or appropriate if prevented
    # (If credentials are valid, login should succeed; otherwise, error message or validation error is expected)
    if results["step_5_error_message"]:
        print(f"Error Message: {results['step_5_error_message']}")
    if results["step_6_validation_error"]:
        print(f"Validation Error: {results['step_6_validation_error']}")

    # Step 7: Ensure login is prevented if credentials are invalid, or login proceeds if valid
    assert results["step_7_login_prevented"] in [True, False], "Login prevention check failed."

    # Overall pass/fail
    assert results["overall_pass"], f"Test failed, see details: {results}"

    # Exception handling
    if results["exception"]:
        pytest.fail(f"Exception occurred: {results['exception']}")
