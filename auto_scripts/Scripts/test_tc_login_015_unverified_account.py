"""
Test Script: test_tc_login_015_unverified_account.py

Automates TC-LOGIN-015: Login with an unverified account and validate error handling and UI feedback.

- Strictly uses LoginPage PageClass.
- Stepwise assertions for all acceptance criteria.
- Designed for CI/CD and robust error traceability.

Test Data:
    Email: unverified@example.com
    Password: ValidPass123!
"""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.mark.usefixtures("setup")
class TestLoginUnverifiedAccount:
    def test_tc_login_015_unverified_account(self):
        """
        TC-LOGIN-015: Verifies login attempt with an unverified account.
        Acceptance Criteria:
            - Login page is displayed.
            - Email is entered.
            - Password is entered and masked.
            - Error message is displayed: 'Please verify your email address before logging in.'
            - User remains on login page with option to resend verification email.
        """
        email = "unverified@example.com"
        password = "ValidPass123!"
        driver = self.driver
        login_page = LoginPage(driver)
        result = login_page.run_tc_login_015_unverified_account(email, password)

        # Step 1: Login page is displayed
        assert result["step_1_navigate_login"] is True, f"Step 1 failed: {result.get('exception', '')}"
        # Step 2: Email is entered
        assert result["step_2_enter_unverified_email"] is True, "Step 2 failed: Email not entered."
        # Step 3: Password is entered
        assert result["step_3_enter_password"] is True, "Step 3 failed: Password not entered."
        # Step 4: Error message is displayed
        assert result["step_4_click_login"] is True, "Step 4 failed: Login button not clicked."
        assert result["step_5_error_message"] is not None, "Step 4 failed: No error message displayed."
        expected_error = "Please verify your email address before logging in."
        assert expected_error.lower() in result["step_5_error_message"].lower(), (
            f"Step 4 failed: Error message mismatch. Found: {result['step_5_error_message']}"
        )
        # Step 5: User remains on login page with resend verification option
        assert result["step_6_resend_verification_option"] is True, "Step 5 failed: Resend verification option missing."
        assert result["step_7_login_prevented"] is True, "Step 5 failed: User is not on login page after failed login."
        # Overall pass
        assert result["overall_pass"] is True, f"Test failed overall: {result}"

# --- Pytest Fixture for Driver Setup/Teardown ---
import sys
import os
import time

@pytest.fixture(scope="class")
def setup(request):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(1440, 900)
    request.cls.driver = driver
    yield
    driver.quit()
