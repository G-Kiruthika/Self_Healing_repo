# Test Case: TC_LOGIN_001 - Valid Login
# This test script uses the LoginPage Page Object to automate the login functionality.
# Test Steps:
# 1. Navigate to the login page
# 2. Enter valid email address
# 3. Enter valid password
# 4. Click on the Login button
# 5. Verify user is logged in (dashboard and user profile displayed)

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage
import time

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')  # Run in headless mode for CI
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_valid_login(driver):
    """
    Test Case ID: TC_LOGIN_001
    Description: Valid login with correct credentials
    """
    login_page = LoginPage(driver)

    # Step 1: Navigate to the login page
    login_page.go_to_login_page()
    assert login_page.is_login_fields_visible(), "Login fields are not visible."

    # Step 2: Enter valid email address
    email = "testuser@example.com"
    assert login_page.enter_email(email), f"Failed to enter email: {email}"

    # Step 3: Enter valid password
    password = "ValidPass123!"
    assert login_page.enter_password(password), "Password field is not masked or input failed."

    # Step 4: Click on the Login button
    login_page.click_login()
    time.sleep(2)  # Wait for redirect, adjust as needed for actual app response time

    # Step 5: Verify user is logged in
    assert login_page.is_redirected_to_dashboard(), "User was not redirected to dashboard."
    assert login_page.is_session_token_created(), "Session token was not created or user profile not visible."
