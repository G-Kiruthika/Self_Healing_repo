#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Script for TC_LOGIN_007: End-to-End Username Recovery Workflow
Traceability:
- TestCaseID: 200
- TestCaseDescription: Test Case TC_LOGIN_007
- PageClass: UsernameRecoveryPage
- Automation Owner: DevOps Agent
- Standards: Selenium Python, Pytest, Enterprise Traceability
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.UsernameRecoveryPage import UsernameRecoveryPage

# --- MOCK LoginPage for demonstration (replace with real import in prod) ---
class LoginPage:
    LOGIN_URL = "https://app.example.com/login"
    def __init__(self, driver, timeout=10):
        self.driver = driver
    def go_to_login_page(self):
        self.driver.get(self.LOGIN_URL)
    def is_on_login_page(self):
        return self.LOGIN_URL in self.driver.current_url
    def click_forgot_username(self):
        # This selector must be updated to match the real 'Forgot Username' link
        self.driver.find_element_by_link_text("Forgot Username?").click()

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_tc_login_007_username_recovery(driver):
    """
    Automated test for TC_LOGIN_007: End-to-End Username Recovery Workflow
    Steps:
        1. Navigate to login page
        2. Click on 'Forgot Username' link
        3. Enter registered email address
        4. Click on 'Send Username' button
        5. Verify username recovery email is received (mocked)
    """
    # --- Test Data ---
    registered_email = "testuser@example.com"
    # --- Page Objects ---
    login_page = LoginPage(driver)
    username_recovery_page = UsernameRecoveryPage(driver)

    # Step 1: Navigate to login page
    login_page.go_to_login_page()
    assert login_page.is_on_login_page(), "[TC_LOGIN_007][Step 1] Login page is not displayed."

    # Step 2: Click on 'Forgot Username' link
    try:
        login_page.click_forgot_username()
    except Exception as e:
        pytest.fail(f"[TC_LOGIN_007][Step 2] Failed to click 'Forgot Username' link: {e}")
    # Assert redirected to username recovery page
    assert "forgot-username" in driver.current_url, "[TC_LOGIN_007][Step 2] Not redirected to username recovery page."

    # Step 3: Enter registered email address
    try:
        username_recovery_page.enter_email(registered_email)
    except Exception as e:
        pytest.fail(f"[TC_LOGIN_007][Step 3] Failed to enter email: {e}")
    # Optionally, validate the email field has value
    email_field = driver.find_element_by_id("recovery-email")
    assert email_field.get_attribute("value") == registered_email, "[TC_LOGIN_007][Step 3] Email not accepted."

    # Step 4: Click on 'Send Username' button
    try:
        username_recovery_page.submit_recovery()
    except Exception as e:
        pytest.fail(f"[TC_LOGIN_007][Step 4] Failed to click 'Send Username' button: {e}")

    # Step 5: Verify username recovery email is received (mocked by confirmation message)
    confirmation = username_recovery_page.get_confirmation_message()
    error_msg = username_recovery_page.get_error_message()
    assert confirmation is not None, (
        f"[TC_LOGIN_007][Step 5] Success message not displayed. Error: {error_msg}"
    )
    assert "Username sent to your email" in confirmation, (
        f"[TC_LOGIN_007][Step 5] Confirmation text mismatch. Actual: '{confirmation}'"
    )
    # Traceability log
    print(f"[TC_LOGIN_007] Test completed. Confirmation: {confirmation}")
