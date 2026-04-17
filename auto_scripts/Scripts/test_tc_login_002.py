"""
Test Script for TC-LOGIN-002: Negative Login Workflow (Invalid/Unregistered Email)
This test automates the process of attempting to login with an invalid email and verifies proper error handling.

Test Steps:
1. Navigate to the login page
2. Enter invalid/unregistered email
3. Enter any password
4. Click Login button
5. Validate error message 'Invalid email or password' is displayed
6. Validate user remains on login page

Author: Automation (generated)
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.TC_LOGIN_002_TestPage import TC_LOGIN_002_TestPage

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_tc_login_002_negative_login(driver):
    """
    Test Case: TC-LOGIN-002 - Negative login with invalid email
    """
    # Test Data
    invalid_email = "invaliduser@example.com"
    password = "SomePassword123"

    # Instantiate the test page class
    test_page = TC_LOGIN_002_TestPage(driver)

    # Run the test workflow
    results = test_page.run_tc_login_002(invalid_email, password)

    # Assertions for each step
    assert results["step_1_navigate_login"], "Step 1 Failed: Login page not displayed."
    assert results["step_2_enter_email"], "Step 2 Failed: Email not entered."
    assert results["step_3_enter_password"], "Step 3 Failed: Password not entered."
    assert results["step_4_click_login"], "Step 4 Failed: Login button not clicked."
    assert results["step_5_error_message"] is not None, "Step 5 Failed: Error message not displayed."
    assert "invalid email or password" in results["step_5_error_message"].lower(), f"Step 5 Failed: Unexpected error message: {results['step_5_error_message']}"
    assert results["step_6_on_login_page"], "Step 6 Failed: User is not on login page after failed login."
    assert results["overall_pass"], f"Test failed: {results.get('exception', '')}"
