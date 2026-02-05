# test_login_invalid_password.py
"""
Automated Selenium Test Script for TC-LOGIN-003: Invalid Password Login

This script validates that attempting to log in with a valid email and invalid password
results in the correct error message and prevents session creation.

Test Steps:
1. Navigate to the login page
2. Enter valid registered email address
3. Enter incorrect password
4. Click on the Login button
5. Verify error message: 'Invalid email or password' and user remains on login page

Author: Automation Generator
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope="function")
def driver():
    # Setup Chrome WebDriver (headless for CI environments)
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_tc_login_003_invalid_password(driver):
    """
    TC-LOGIN-003: Invalid Password Login
    """
    login_page = LoginPage(driver)
    email = "testuser@example.com"
    wrong_password = "WrongPassword456"

    # Step 1: Navigate to login page
    login_page.load()
    assert login_page.is_displayed(), "Login page is not displayed"

    # Step 2: Enter valid registered email
    login_page.enter_email(email)

    # Step 3: Enter incorrect password
    login_page.enter_password(wrong_password)

    # Step 4: Click on Login button
    login_page.click_login()

    # Step 5: Verify error message and user remains on login page
    error_message = login_page.get_error_message()
    assert error_message is not None, "No error message displayed after invalid login attempt"
    assert "Invalid email or password" in error_message, (
        f"Expected 'Invalid email or password' error message, got: {error_message}"
    )
    assert not login_page.is_dashboard_displayed(), "Dashboard should not be displayed for invalid login"
    assert not login_page.is_user_profile_icon_displayed(), "User profile icon should not be visible for invalid login"
    # Optionally check for session cookie (if implemented)
    # cookies = driver.get_cookies()
    # assert not any(c['name'] == 'sessionid' for c in cookies), "Session cookie should not be present after failed login"

    print("TC-LOGIN-003 passed: Invalid password error message validated and session not created.")
