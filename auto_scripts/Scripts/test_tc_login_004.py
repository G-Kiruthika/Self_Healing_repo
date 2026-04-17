# test_tc_login_004.py
"""
Selenium test script for TC-LOGIN-004: Attempt login with empty email and valid password.
Validates error handling and login prevention as per test case.
"""
import sys
import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.TC_LOGIN_004_TestPage import TC_LOGIN_004_TestPage

@pytest.fixture(scope='module')
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

@pytest.mark.tc_login_004
def test_tc_login_004(driver):
    """
    Test Case TC-LOGIN-004: Leave email field empty, enter valid password, attempt login.
    Verifies validation error and prevention of authentication.
    """
    # Arrange
    valid_password = "ValidPass123!"
    login_url = "https://ecommerce.example.com/login"
    page = TC_LOGIN_004_TestPage(driver)

    # Act
    results = page.run_tc_login_004(password=valid_password, url=login_url)

    # Assert: Step 1 - Login page is displayed
    assert results["step_1_navigate_login"] is True, f"Failed to display login page: {results['exception']}"
    # Assert: Step 2 - Email field remains blank (implicit by PageClass)
    assert results["step_2_leave_email_empty"] is True, "Email field was not left empty."
    # Assert: Step 3 - Password entered and masked (cannot check mask, but input sent)
    assert results["step_3_enter_password"] is True, "Password was not entered."
    # Assert: Step 4 - Click login
    assert results["step_4_click_login"] is True, "Login button was not clicked."
    # Assert: Step 5 - Validation error displayed
    assert results["step_5_validation_error"] is not None and results["step_5_validation_error"].strip() != "", \
        "Validation error not displayed when email is empty."
    # Assert: Step 6 - User remains on login page (login prevented)
    assert results["step_6_login_prevented"] is True, "User did not remain on login page after failed login."
    # Assert: Overall pass
    assert results["overall_pass"] is True, f"Test did not pass overall: {results}"

    print("TC-LOGIN-004 executed successfully.")
