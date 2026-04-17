'''
Test Script for TC-LOGIN-002: Negative Login Workflow (Invalid/Unregistered Email)
Author: Automation Agent
Description: Uses TC_LOGIN_002_TestPage to automate and validate negative login scenario.
'''
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.TC_LOGIN_002_TestPage import TC_LOGIN_002_TestPage

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_tc_login_002_negative_login(driver):
    """
    Test Case TC-LOGIN-002: Negative Login with Invalid/Unregistered Email
    Steps:
        1. Navigate to login page
        2. Enter invalid email and any password
        3. Click Login
        4. Verify error message
        5. Verify user remains on login page
    """
    # Test Data
    invalid_email = "invaliduser@example.com"
    password = "SomePassword123"
    # Instantiate PageClass
    tc_login_002 = TC_LOGIN_002_TestPage(driver)
    # Run test workflow
    results = tc_login_002.run_tc_login_002(invalid_email, password)
    # Stepwise assertions
    assert results["step_1_navigate_login"], f"Step 1 failed: Login page not displayed. Exception: {results.get('exception')}"
    assert results["step_2_enter_email"], "Step 2 failed: Unable to enter invalid email."
    assert results["step_3_enter_password"], "Step 3 failed: Unable to enter password."
    assert results["step_4_click_login"], "Step 4 failed: Login button click failed."
    assert results["step_5_error_message"] is not None, "Step 5 failed: Error message not displayed."
    assert "invalid email or password" in results["step_5_error_message"].lower(), f"Step 5 failed: Unexpected error message: {results['step_5_error_message']}"
    assert results["step_6_on_login_page"], "Step 6 failed: User is not on login page after failed login."
    assert results["overall_pass"], f"Test failed overall. Exception: {results.get('exception')}"
