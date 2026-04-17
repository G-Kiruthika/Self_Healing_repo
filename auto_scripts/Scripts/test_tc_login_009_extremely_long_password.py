# test_tc_login_009_extremely_long_password.py
"""
Test Script for TC-LOGIN-009: Extremely Long Password Input
This script uses the LoginPage PageClass to validate system behavior for a password input exceeding 1000 characters.

Acceptance Criteria (TS-007):
- The system must either truncate the input or display a validation error.
- Login must fail gracefully, with an appropriate error message and no user authentication.

Test Data:
- URL: https://ecommerce.example.com/login
- Email: testuser@example.com
- Password: <A string of 1000+ characters>
"""

import sys
import os
import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage

# Test configuration
LOGIN_URL = "https://ecommerce.example.com/login"
TEST_EMAIL = "testuser@example.com"
VERY_LONG_PASSWORD = "VeryLongPassword" * 100  # 1700+ chars

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_tc_login_009_extremely_long_password(driver):
    """
    TC-LOGIN-009: Test login with an extremely long password.
    """
    login_page = LoginPage(driver)
    results = login_page.run_tc_login_009_extremely_long_password(TEST_EMAIL, VERY_LONG_PASSWORD)

    # Step 1: Login page is displayed
    assert results["step_1_navigate_login"], "Login page was not displayed."

    # Step 2: Email entered
    assert results["step_2_enter_email"], "Email was not entered correctly."

    # Step 3: Long password entered
    assert results["step_3_enter_long_password"], "Long password was not entered."

    # Step 4: Clicked login
    assert results["step_4_click_login"], "Login button was not clicked."

    # Step 5: Expect error message or validation error
    error_msg = results["step_5_error_message"]
    validation_msg = results["step_6_validation_error"]
    assert (error_msg or validation_msg), (
        "Neither error message nor validation message was shown for extremely long password."
    )

    # Step 6: Ensure login is prevented (still on login page)
    assert results["step_7_login_prevented"], (
        "User was not prevented from logging in with extremely long password."
    )

    # Step 7: Overall test pass
    assert results["overall_pass"], (
        f"Test failed. Results: {results}"
    )

    # Optional: Print error/validation message for traceability
    print("Error Message:", error_msg)
    print("Validation Message:", validation_msg)

if __name__ == "__main__":
    pytest.main([__file__])
