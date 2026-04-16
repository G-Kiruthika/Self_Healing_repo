"""
Test Script for TC_LOGIN_018: Login with valid email and three incorrect passwords

This script validates that after three failed login attempts with a valid email and wrong passwords,
a warning message is displayed: 'Warning: Account will be locked after 2 more failed attempts'.

- Follows enterprise Selenium Python automation standards.
- Asserts all critical steps and outputs detailed errors for traceability.
- Designed for CI/CD integration and maintainability.

Author: Automation Bot
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from auto_scripts.Pages.TC_LOGIN_018_TestPage import TC_LOGIN_018_TestPage

# Test Data
LOGIN_URL = "https://app.example.com/login"
VALID_EMAIL = "testuser@example.com"
WRONG_PASSWORDS = ["WrongPass1", "WrongPass2", "WrongPass3"]
EXPECTED_WARNING = "Warning: Account will be locked after 2 more failed attempts"

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_tc_login_018(driver):
    """
    End-to-end test for TC_LOGIN_018 using the PageClass abstraction.
    """
    test_page = TC_LOGIN_018_TestPage(driver)
    results = test_page.run_tc_login_018(VALID_EMAIL, WRONG_PASSWORDS)

    # Step 1: Login page displayed
    assert results["step_1_navigate_login"] is True, f"Step 1 failed: Login page not displayed. Exception: {results.get('exception')}"

    # Step 2: Email entered
    assert results["step_2_enter_email"] is True, "Step 2 failed: Email not entered."

    # Step 3: Each attempt fails
    assert len(results["step_3_attempts"]) == 3, f"Step 3 failed: Expected 3 attempts, got {len(results['step_3_attempts'])}."
    for idx, attempt in enumerate(results["step_3_attempts"]):
        assert attempt["failed"], f"Step 3 failed: Attempt {idx+1} did not fail as expected. Error message: {attempt['error_message']}"
        assert attempt["error_message"] is not None, f"Step 3 failed: No error message on attempt {idx+1}."

    # Step 4: Warning message displayed
    warning_msg = results["step_4_warning_message"]
    assert warning_msg is not None, "Step 4 failed: Warning message not displayed after third failed attempt."
    assert EXPECTED_WARNING in warning_msg, f"Step 4 failed: Warning message mismatch. Found: {warning_msg}"

    # Overall Pass
    assert results["overall_pass"] is True, f"Test failed overall. Exception: {results.get('exception')}"
