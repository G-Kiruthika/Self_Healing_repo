# -*- coding: utf-8 -*-
"""
Automated Selenium Test Script for TC-LOGIN-008: Login with extremely long email address
Author: Automation Agent
Date: 2024-06-10
Traceability: testCaseId=235
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_tc_login_008_extremely_long_email(driver):
    """
    TC-LOGIN-008: Login with extremely long email address (255+ characters)
    Steps:
        1. Navigate to the login page
        2. Enter an extremely long email address
        3. Enter valid password
        4. Click on the Login button
        5. Verify system truncates input or shows validation error, or login fails gracefully
    """
    # Test Data
    extremely_long_email = (
        "verylongemailaddressverylongemailaddressverylongemailaddress"
        "verylongemailaddressverylongemailaddressverylongemailaddress"
        "verylongemailaddressverylongemailaddressverylongemailaddress"
        "verylongemailaddressverylongemailaddressverylongemailaddress"
        "@example.com"
    )
    valid_password = "ValidPass123!"

    login_page = LoginPage(driver)

    # Step 1: Navigate to login page
    login_page.go_to_login_page()
    assert login_page.is_loaded(), "Step 1 Failed: Login page is not displayed."

    # Step 2: Enter extremely long email address
    email_entered = login_page.enter_email(extremely_long_email)
    assert email_entered, "Step 2 Failed: Email input value does not match test data."

    # Step 3: Enter valid password
    password_entered = login_page.enter_password(valid_password)
    assert password_entered, "Step 3 Failed: Password input value does not match test data."

    # Step 4: Click Login
    login_page.click_login()

    # Step 5: Verify error message, validation error, or login fails gracefully
    validation_error = login_page.is_validation_error_displayed()
    error_message = login_page.is_error_message_displayed()
    login_failed = driver.current_url.startswith(login_page.LOGIN_URL)
    assert validation_error or error_message or login_failed, (
        "Step 5 Failed: Expected validation error, error message, or failed login, but none detected."
    )

    # Traceability
    print(f"TestCaseID: 235 | TC-LOGIN-008 | Extremely long email: {extremely_long_email[:30]}... | Result: PASSED")
