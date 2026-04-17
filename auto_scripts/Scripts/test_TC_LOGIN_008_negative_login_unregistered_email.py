# test_TC_LOGIN_008_negative_login_unregistered_email.py
"""
Automated Selenium Test Script for TC-LOGIN-008: Negative Login (Unregistered Email)
This test verifies that attempting to log in with an unregistered email displays the correct error message and the user is not authenticated.

Test Steps:
1. Navigate to login page
2. Enter unregistered email
3. Enter any password
4. Click Login
5. Assert error message is displayed
6. Assert user remains on login page

Author: Automation (Generated)
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from auto_scripts.Pages.TC_LOGIN_002_TestPage import TC_LOGIN_002_TestPage

# Test Data (parameterize as needed)
LOGIN_URL = "https://app.example.com/login"
INVALID_EMAIL = "unregistered@example.com"
PASSWORD = "AnyPass123!"
EXPECTED_ERROR = "Invalid email or password"

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_tc_login_008_negative_login_unregistered_email(driver):
    """
    TC-LOGIN-008: Attempt login with unregistered email, expect error and no authentication.
    """
    # Instantiate the PageClass
    test_page = TC_LOGIN_002_TestPage(driver)
    # Navigate to login page (step 1)
    driver.get(LOGIN_URL)
    # Run the test case logic (steps 2-6)
    results = test_page.run_tc_login_002(INVALID_EMAIL, PASSWORD)
    # Stepwise assertions
    assert results["step_1_navigate_login"], "Login page should be displayed."
    assert results["step_2_enter_email"], "Should be able to enter email."
    assert results["step_3_enter_password"], "Should be able to enter password."
    assert results["step_4_click_login"], "Should be able to click login button."
    assert results["step_5_error_message"] is not None, "Error message should be displayed."
    assert EXPECTED_ERROR.lower() in results["step_5_error_message"].lower(), \
        f"Expected error message '{EXPECTED_ERROR}', got '{results['step_5_error_message']}'"
    assert results["step_6_on_login_page"], "User should remain on login page after failed login."
    assert results["overall_pass"], f"Test failed. Details: {results}"
