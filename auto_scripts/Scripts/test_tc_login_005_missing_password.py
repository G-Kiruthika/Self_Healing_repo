# Selenium Test Script for TC-LOGIN-005: Login Attempt with Missing Password and Validation Error
# This script uses the LoginPage PageClass (auto_scripts/Pages/LoginPage.py) for test execution.
# Test Case Reference: TC-LOGIN-005
# Author: Automation Generator
#
# Steps:
# 1. Navigate to the login page
# 2. Enter valid email address
# 3. Leave password field empty
# 4. Click Login
# 5. Assert validation error is displayed
# 6. Assert user is not authenticated and remains on login page

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import AssertionError
import time
import sys
import os

# Ensure the PageClass is importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Pages')))
from LoginPage import LoginPage

@pytest.fixture(scope='function')
def driver():
    # Setup Chrome WebDriver (headless for CI/CD)
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_tc_login_005_missing_password(driver):
    """
    Test Case: TC-LOGIN-005
    Title: Login Attempt with Missing Password and Validation Error
    Steps:
        1. Navigate to the login page
        2. Enter valid email address (testuser@example.com)
        3. Leave password field empty
        4. Click Login
        5. Assert validation error is displayed
        6. Assert user remains on login page
    Acceptance Criteria: TS-003
    """
    login_page = LoginPage(driver)
    email = "testuser@example.com"

    # Step 1-6: Execute the PageClass method (includes all asserts)
    try:
        result = login_page.tc_login_005_missing_password_validation(email)
        assert result is True, "Test step returned False, expected True."
    except AssertionError as ae:
        pytest.fail(str(ae))
    except Exception as e:
        pytest.fail(f"Unexpected error during TC-LOGIN-005: {str(e)}")
