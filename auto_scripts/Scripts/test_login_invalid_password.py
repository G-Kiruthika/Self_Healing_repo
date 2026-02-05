# test_login_invalid_password.py
"""
Automated Selenium Test Script for TC-LOGIN-003: Invalid Password Login

Test Case Reference: TC-LOGIN-003
Test Description:
1. Navigate to the login page [Test Data: URL: https://ecommerce.example.com/login]
2. Enter valid registered email address [Test Data: Email: testuser@example.com]
3. Enter incorrect password [Test Data: Password: WrongPassword456]
4. Click on the Login button
5. Verify error message: 'Invalid email or password' and user remains on login page (no session created)

Traceability:
- PageClass: LoginPage (auto_scripts/Pages/LoginPage.py)
- Method: tc_login_003_invalid_password_error_message
- TestCase ID: 230

Acceptance Criteria:
- Error message is displayed: 'Invalid email or password'
- User is not logged in and no session is created

Author: Automated by Test Automation Agent
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1440, 900)
    yield driver
    driver.quit()

def test_tc_login_003_invalid_password(driver):
    """
    TC-LOGIN-003: Invalid Password Login
    Steps:
    1. Navigate to the login page
    2. Enter valid registered email address
    3. Enter incorrect password
    4. Click on the Login button
    5. Verify error message: 'Invalid email or password' and user remains on login page (no session created)
    """
    login_page = LoginPage(driver)
    # Test Data
    valid_email = "testuser@example.com"
    wrong_password = "WrongPassword456"

    # Step 1: Navigate to login page
    login_page.load()
    assert login_page.is_displayed(), "[TC-LOGIN-003][Step 1] Login page is not displayed"

    # Step 2: Enter valid registered email
    login_page.enter_email(valid_email)
    # Step 3: Enter incorrect password
    login_page.enter_password(wrong_password)
    # Step 4: Click Login
    login_page.click_login()

    # Step 5: Validate error message and session state
    error = login_page.get_error_message()
    assert error is not None, "[TC-LOGIN-003][Step 5] No error message displayed after invalid login attempt"
    assert "Invalid email or password" in error, f"[TC-LOGIN-003][Step 5] Expected 'Invalid email or password' error message, got: {error}"

    # Ensure user remains on login page (no dashboard/profile icon)
    assert not login_page.is_dashboard_displayed(), "[TC-LOGIN-003][Step 5] Dashboard should not be displayed for invalid login"
    assert not login_page.is_user_profile_icon_displayed(), "[TC-LOGIN-003][Step 5] User profile icon should not be visible for invalid login"

    # Optionally: Check for absence of session cookies (if implemented)
    # cookies = driver.get_cookies()
    # assert not any(c['name'] == 'sessionid' for c in cookies), "[TC-LOGIN-003][Step 5] Session cookie should not be present after failed login"
