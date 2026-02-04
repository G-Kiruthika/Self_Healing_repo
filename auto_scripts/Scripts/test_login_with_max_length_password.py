#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Selenium Automated Test Script for TC_LOGIN_013: Login with Maximum Length Password (128 chars)
Generated automatically from PageClass definition and requirements.
Traceability: testCaseId=142, testCase=TC_LOGIN_013
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import AssertionError, WebDriverException
import time
import string
import random

from auto_scripts.Pages.LoginPage import LoginPage

def generate_max_length_password():
    # Example: 128 chars, repeat pattern for deterministic output
    return "Aa1!" * 32  # 4*32=128

def get_valid_email():
    return "testuser@example.com"

@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_with_max_length_password(driver):
    """
    Test Case TC_LOGIN_013:
    1. Navigate to the login page
    2. Enter valid email address
    3. Enter password at maximum allowed length (128 characters)
    4. Click Login button
    5. Assert login is processed without validation error
    """
    login_page = LoginPage(driver)
    email = get_valid_email()
    password = generate_max_length_password()

    # Step 1: Navigate to login page
    login_page.go_to_login_page()
    assert driver.current_url.startswith("https://app.example.com/login"), "Login page URL mismatch!"
    assert login_page.is_login_fields_visible(), "Login fields are not visible!"

    # Step 2: Enter valid email
    assert login_page.enter_email(email), "Email was not entered correctly!"

    # Step 3: Enter max length password (128 chars)
    assert len(password) == 128, f"Password length is not 128, got {len(password)}"
    assert login_page.enter_password(password), "Password was not entered/masked correctly!"

    # Step 4: Click Login
    login_page.click_login()
    time.sleep(1)  # Wait for response

    # Step 5: Assert no validation error
    error_message = login_page.get_error_message()
    assert error_message is None or error_message == "", f"Unexpected error message: {error_message}"
    # Optionally, assert that login is processed (e.g., redirected or session created)
    # assert login_page.is_redirected_to_dashboard() or login_page.is_session_token_created(), "Login not processed as expected!"

    print("TC_LOGIN_013: Login with max length password executed successfully.")
