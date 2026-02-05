#!/usr/bin/env python3
"""
Selenium Automation Test Script for TC_LOGIN_005
Covers: Attempt login with both email and password fields empty, validate error messages and prevention of login.
Author: AutomationBot
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_empty_fields(driver):
    """
    Test Case: TC_LOGIN_005
    Steps:
      1. Navigate to the login page
      2. Leave email field empty
      3. Leave password field empty
      4. Click on the Login button
      5. Verify login is prevented and validation errors are displayed
    """
    login_page = LoginPage(driver)

    # Step 1: Navigate to the login page
    assert login_page.navigate_to_login(), "Login page is not displayed."

    # Step 2 & 3: Leave email and password fields empty
    fields_empty = login_page.leave_email_and_password_empty()
    assert fields_empty, "Email and/or Password fields are not empty."

    # Step 4: Click on Login and verify validation errors
    errors_present = login_page.click_login_and_verify_required_errors()
    assert errors_present, "Validation errors for required fields not displayed."

    # Step 5: Verify login is prevented and user remains on login page
    login_prevented = login_page.verify_login_prevented_empty_fields()
    assert login_prevented, "Login was not prevented or user did not remain on login page."

    print("TC_LOGIN_005: Passed - Required field validation and login prevention verified.")
