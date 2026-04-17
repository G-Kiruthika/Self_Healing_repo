#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Script for TC-LOGIN-003: Forgot Username Workflow and Negative Login
Author: Automation Agent

Test Steps:
1. Navigate to the login page
2. Enter valid registered email address
3. Enter incorrect password
4. Click Login
5. Assert error message
6. Assert user remains on login page
7. Initiate Forgot Username workflow and assert confirmation

Dependencies: Selenium, pytest, Pages (LoginPage, UsernameRecoveryPage, TC_LOGIN_003_TestPage)
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage
from auto_scripts.Pages.UsernameRecoveryPage import UsernameRecoveryPage
from auto_scripts.Pages.TC_LOGIN_003_TestPage import TC_LOGIN_003_TestPage

EMAIL = "testuser@example.com"
WRONG_PASSWORD = "WrongPassword456"
LOGIN_URL = "https://example-ecommerce.com/login"
FORGOT_USERNAME_RECOVERY_EMAIL = EMAIL  # Using same email for recovery

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

@pytest.mark.tc_login_003
class TestTC_LOGIN_003:
    def test_login_with_wrong_password(self, driver):
        """
        Steps 1-6: Attempt login with incorrect password and validate error handling.
        """
        login_page = LoginPage(driver)
        # Step 1: Navigate to login page
        login_page.go_to_login_page()
        assert login_page.is_on_login_page(), "Login page is not displayed (Step 2)"
        # Step 3: Enter valid email
        login_page.enter_email(EMAIL)
        # Step 4: Enter incorrect password
        login_page.enter_password(WRONG_PASSWORD)
        # Step 5: Click Login
        login_page.click_login()
        # Step 5: Assert error message
        error_msg = login_page.get_error_message()
        assert error_msg is not None, "No error message displayed after invalid login (Step 5)"
        assert "invalid" in error_msg.lower(), f"Unexpected error message: {error_msg}"
        # Step 6: Assert user remains on login page
        assert login_page.is_on_login_page(), "User was redirected away from login page after failed login (Step 6)"

    def test_forgot_username_workflow(self, driver):
        """
        Step 7: Click 'Forgot Username', recover username and assert confirmation message.
        """
        # Use orchestrator PageClass for end-to-end flow
        tc_page = TC_LOGIN_003_TestPage(driver)
        results = tc_page.execute_tc_login_003(FORGOT_USERNAME_RECOVERY_EMAIL)
        # Step 1: Navigated to login page
        assert results["step_1_navigate_login"] is True, f"Failed to navigate to login page: {results['exception']}"
        # Step 2: Clicked 'Forgot Username'
        assert results["step_2_forgot_username_clicked"] is True, f"Failed to click 'Forgot Username': {results['exception']}"
        # Step 3: Username recovery successful
        assert results["step_3_recovery_success"] is True, f"Username recovery failed: {results['error_message']}"
        # Confirmation message present
        assert results["confirmation_message"] is not None, "No confirmation message after username recovery"
        # Overall test pass
        assert results["overall_pass"] is True, f"Overall test did not pass: {results['exception']}"
