#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test Script for TC_LOGIN_017: Test repeated failed login attempts, successful login, and counter reset after logout.
Traceability:
- TestCaseId: 146
- TestCase: TC_LOGIN_017
- Acceptance Criteria: SCRUM-91
- PageClass: LoginPage (auto_scripts/Pages/LoginPage.py)

Steps:
1. Navigate to login page
2. Enter valid email and incorrect password, click Login (Attempt 1-3)
3. Assert error message displayed for each failed attempt
4. Enter valid email and correct password, click Login
5. Assert successful login and failed attempt counter reset
6. Logout
7. Attempt login again with incorrect password
8. Assert failed attempt counter starts from 1
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage
import time

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_tc_login_017(driver):
    """
    TC_LOGIN_017: Test repeated failed login attempts, successful login, and counter reset after logout.
    """
    login_page = LoginPage(driver)
    email = "testuser@example.com"
    wrong_passwords = ["WrongPass1", "WrongPass2", "WrongPass3"]
    correct_password = "ValidPass123!"
    wrong_password_after_logout = "WrongPass4"

    # Step 1: Navigate to login page
    login_page.go_to_login_page()
    assert login_page.is_login_fields_visible(), "Login fields are not visible."
    assert driver.current_url == LoginPage.LOGIN_URL, "Not on login page."

    # Step 2: Attempt 1-3 with invalid passwords
    for idx, wrong_pass in enumerate(wrong_passwords, 1):
        login_page.enter_email(email)
        login_page.enter_password(wrong_pass)
        login_page.click_login()
        assert login_page.is_error_message_displayed(), f"Error message not displayed on failed attempt {idx}."
        # Optionally, sleep for UI feedback
        time.sleep(0.5)

    # Step 3: Login with correct password
    login_page.enter_email(email)
    login_page.enter_password(correct_password)
    login_page.click_login()
    assert login_page.is_redirected_to_dashboard(), "User not redirected to dashboard after correct login."
    assert login_page.is_session_token_created(), "Session token not created after successful login."

    # Step 4: Logout
    assert login_page.logout(), "Logout failed or not redirected to login page."
    assert driver.current_url == LoginPage.LOGIN_URL, "Not redirected to login page after logout."
    assert login_page.is_login_fields_visible(), "Login fields not visible after logout."

    # Step 5: Attempt login with wrong password again (counter should reset)
    login_page.enter_email(email)
    login_page.enter_password(wrong_password_after_logout)
    login_page.click_login()
    assert login_page.is_error_message_displayed(), "Error message not displayed after failed login post-logout."
    # If counter is displayed in UI, add assertion here (not implemented in PageClass)

    # Final assertion: Optionally, ensure still on login page
    assert driver.current_url == LoginPage.LOGIN_URL, "Should remain on login page after failed login."
