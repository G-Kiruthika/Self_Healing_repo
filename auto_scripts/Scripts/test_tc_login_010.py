import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.TC_LOGIN_010_TestPage import TC_LOGIN_010_TestPage

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_tc_login_010(driver):
    """
    Test Case ID: 206 / TC_LOGIN_010
    Description: Login with maximum valid email length (254 chars), valid password, verify system behavior.
    """
    # Test Data
    max_email = "a234567890123456789012345678901234567890123456789012345678901234@b234567890123456789012345678901234567890123456789012345678901234.c234567890123456789012345678901234567890123456789012345678901234.d234567890123456789012345678901234567890123456789012345678.com"
    valid_password = "ValidPass123!"

    page = TC_LOGIN_010_TestPage(driver)
    results = page.run_tc_login_010(max_email, valid_password)

    # Step 1: Navigate to login page
    assert results["step_1_navigate_login"], f"Step 1 failed: Login page not displayed. Exception: {results['exception']}"
    # Step 2: Enter maximum valid length email
    assert results["step_2_enter_email"], "Step 2 failed: Email was not accepted."
    # Step 3: Enter valid password
    assert results["step_3_enter_password"], "Step 3 failed: Password was not accepted."
    # Step 4: Click Login button
    assert results["step_4_click_login"], "Step 4 failed: Login button could not be clicked."
    # Step 5: Check for error message (should be None for valid input)
    assert results["step_5_error_message"] is None, f"Step 5 failed: Unexpected error message: {results['step_5_error_message']}"
    # Step 6: Check for validation error (should be None for valid input)
    assert results["step_6_validation_error"] is None, f"Step 6 failed: Unexpected validation error: {results['step_6_validation_error']}"
    # Step 7: Ensure login is handled appropriately (remains on page or successful auth, no errors)
    assert results["step_7_login_prevented"], "Step 7 failed: System did not handle boundary email correctly."
    # Overall pass
    assert results["overall_pass"], f"Test did not pass overall. Exception: {results['exception']}"
