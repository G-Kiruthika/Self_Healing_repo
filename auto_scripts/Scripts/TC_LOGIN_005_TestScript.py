# TC_LOGIN_005_TestScript.py
"""
Selenium Automation Test Script for TC-LOGIN-005: Valid email, empty password, validate error message and login prevention.
This script uses the TC_LOGIN_005_TestPage PageClass and asserts each step as per enterprise standards.
"""

import pytest
from selenium import webdriver
from auto_scripts.Pages.TC_LOGIN_005_TestPage import TC_LOGIN_005_TestPage

@pytest.mark.usefixtures("driver_init")
def test_tc_login_005_negative_login(driver):
    """
    Test Case: TC-LOGIN-005
    Steps:
        1. Navigate to login page
        2. Enter valid email
        3. Leave password field empty
        4. Click Login button
        5. Validate error message 'Password is required'
        6. Ensure user remains on login page
    """
    # --- Test Data ---
    test_email = "testuser@example.com"
    login_url = "https://ecommerce.example.com/login"

    page = TC_LOGIN_005_TestPage(driver)
    results = page.run_tc_login_005(test_email, login_url)

    # --- Stepwise Assertions ---
    assert results["step_1_navigate_login"] is True, "Login page did not load correctly."
    assert results["step_2_enter_email"] is True, "Email was not entered."
    assert results["step_3_leave_password_empty"] is True, "Password field was not cleared."
    assert results["step_4_click_login"] is True, "Login button was not clicked."
    assert results["step_5_validation_error"] is not None, "Validation error not displayed."
    assert "password is required" in results["step_5_validation_error"].lower(), (
        f"Expected error message 'Password is required', got: {results['step_5_validation_error']}"
    )
    assert results["step_6_login_prevented"] is True, "User did not remain on login page after failed login."
    assert results["overall_pass"] is True, (
        f"Overall test failed. Exception: {results['exception']}"
    )

# --- Pytest Fixture for WebDriver ---
import pytest

@pytest.fixture(scope="function")
def driver_init(request):
    driver = webdriver.Chrome()
    driver.maximize_window()
    request.cls.driver = driver
    yield driver
    driver.quit()
