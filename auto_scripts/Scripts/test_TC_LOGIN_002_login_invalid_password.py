# File: auto_scripts/Scripts/test_TC_LOGIN_002_login_invalid_password.py

"""
Test Case: TC_LOGIN_002 - Invalid Password Login Attempt
This script verifies that a user cannot log in with a valid email and an incorrect password,
and that the correct error message is displayed while the user remains on the login page.

Test Steps:
1. Navigate to the login page.
2. Enter valid registered email.
3. Enter incorrect password.
4. Click on the Login button.
5. Verify user remains on login page and error message is displayed.

Author: Automation Generator
"""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from auto_scripts.Pages.LoginPage import LoginPage
import time

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument("--headless")  # Run in headless mode for CI/CD
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_TC_LOGIN_002_invalid_password(driver):
    """
    TC_LOGIN_002: Login with valid email and incorrect password.
    """
    login_page = LoginPage(driver)

    # Step 1: Navigate to the login page
    assert login_page.navigate_to_login(), "Login page is not displayed"

    # Step 2: Enter valid registered email
    email = "testuser@example.com"
    assert login_page.enter_email(email), f"Email '{email}' was not accepted in the email field"

    # Step 3: Enter incorrect password
    incorrect_password = "WrongPass456!"
    assert login_page.enter_incorrect_password(incorrect_password), "Password is not masked or not accepted in the password field"

    # Step 4: Click on the Login button and verify error message
    expected_error = "Invalid email or password"
    assert login_page.click_login_and_check_error(), f"Error message '{expected_error}' not displayed after failed login"

    # Step 5: Verify user remains on login page
    assert login_page.verify_user_stays_on_login_page(), "User is not on login page after failed login"

    # Optionally, ensure dashboard is NOT displayed
    assert not login_page.is_dashboard_displayed(), "Dashboard should not be visible after failed login"

# End of test_TC_LOGIN_002_login_invalid_password.py
