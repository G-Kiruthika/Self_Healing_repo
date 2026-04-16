# Test Script for TC_LOGIN_018: Multiple Failed Login Attempts & Warning Message
# Traceability: testCaseId=155, Acceptance Criteria=AC_009
# Author: Automation Generator
#
# This test validates that after three failed login attempts, the appropriate warning message is displayed.

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.mark.usefixtures("driver_init")
class TestTCLogin018:
    """
    Test Case: TC_LOGIN_018
    Title: Multiple Failed Login Attempts & Warning Message
    Traceability: testCaseId=155
    Acceptance Criteria: AC_009
    """

    def test_multiple_failed_login_attempts_warning(self, driver):
        # Test Data
        email = "testuser@example.com"
        wrong_passwords = ["WrongPass1", "WrongPass2", "WrongPass3"]
        expected_warning = "Warning: Account will be locked after 2 more failed attempts"

        # Step 1: Instantiate LoginPage
        login_page = LoginPage(driver)

        # Step 2-4: Run the workflow
        results = login_page.run_tc_login_018(email, wrong_passwords)

        # Step 1 Assertion: Login page is displayed
        assert results["step_1_navigate_login"] is True, "Login page should be displayed."
        # Step 2 Assertion: Email is entered
        assert results["step_2_enter_email"] is True, "Email field should accept input."
        # Step 3 Assertion: Each attempt fails
        assert len(results["step_3_attempts"]) == 3, "There should be 3 login attempts."
        for idx, attempt in enumerate(results["step_3_attempts"]):
            assert attempt["error_message"] is not None, f"Attempt {idx+1}: Error message should be displayed."
        # Step 4 Assertion: Warning message after third attempt
        assert results["step_4_warning_message"] is not None, "Warning message should be displayed after third failed attempt."
        assert results["step_4_warning_message"].strip() == expected_warning, (
            f"Expected warning message: '{expected_warning}', got: '{results['step_4_warning_message']}'"
        )
        # Overall pass
        assert results["overall_pass"] is True, f"Test did not pass all validations: {results}"
        # Exception check
        assert results["exception"] is None, f"Exception occurred during test: {results['exception']}"

# --- Pytest Fixture for WebDriver ---
import sys
import os
import time
@pytest.fixture(scope="class")
def driver_init(request):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    request.cls.driver = driver
    yield driver
    driver.quit()
