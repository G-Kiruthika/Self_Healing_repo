#!/usr/bin/env python3
"""
Test Automation Script for TC-LOGIN-009: Login with Extremely Long Password

This script automates the test scenario for attempting to login with a valid email and an extremely long password (1000+ characters).
It uses the LoginPage Page Object (auto_scripts/Pages/LoginPage.py) and validates that the system handles the input gracefully by showing an error, truncating the input, or failing login without unexpected behavior.

Test Data:
    - URL: https://ecommerce.example.com/login
    - Email: testuser@example.com
    - Password: <1000+ character string>

Acceptance Criteria:
    - System either truncates the input, shows a validation error, or fails login gracefully (no crash, no access granted).

Traceability:
    - TestCaseId: 236
    - TestCase: TC-LOGIN-009
    - PageClass: LoginPage
    - Method: tc_login_009_extremely_long_password_login
"""

import sys
import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

# Add PageClass directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../Pages')))
from LoginPage import LoginPage

# --- Test Data ---
LOGIN_URL = "https://ecommerce.example.com/login"
VALID_EMAIL = "testuser@example.com"
VERY_LONG_PASSWORD = "VeryLongPassword" * 67  # 17*67 = 1139 chars

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_tc_login_009_extremely_long_password(driver):
    """
    TC-LOGIN-009: Verify login with extremely long password is handled gracefully.
    Steps:
        1. Navigate to login page.
        2. Enter valid email.
        3. Enter extremely long password (>1000 chars).
        4. Click login.
        5. Assert system response is graceful (error, truncation, or validation message).
    """
    login_page = LoginPage(driver)
    result = login_page.tc_login_009_extremely_long_password_login(VALID_EMAIL, VERY_LONG_PASSWORD)
    assert result, (
        "[TC-LOGIN-009] System did NOT handle extremely long password gracefully: "
        "Expected error, truncation, or validation message. "
        "Check application logs or UI for further details."
    )
