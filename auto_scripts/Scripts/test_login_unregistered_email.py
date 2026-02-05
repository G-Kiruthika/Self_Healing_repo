# Selenium Test Script for TC_LOGIN_008: Login with Unregistered Email
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
import time
import sys
import os

# Import LoginPage from the correct relative path
auto_scripts_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Pages'))
if auto_scripts_dir not in sys.path:
    sys.path.insert(0, auto_scripts_dir)
from LoginPage import LoginPage

# Test Data for TC_LOGIN_008
test_url = "https://app.example.com/login"
test_email = "unregistered@example.com"
test_password = "AnyPass123!"
expected_error = "Invalid email or password"

@pytest.fixture(scope='module')
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_tc_login_008_unregistered_email(driver):
    """
    Test Case: TC_LOGIN_008 - Login attempt with unregistered email
    Steps:
    1. Navigate to the login page
    2. Enter unregistered email address
    3. Enter any password
    4. Click on the Login button
    5. Verify error message: 'Invalid email or password'
    6. Verify user remains on login page
    Acceptance Criteria: AC_008
    """
    login_page = LoginPage(driver)

    # Step 1: Navigate to the login page
    driver.get(test_url)
    assert login_page.is_login_page_displayed(), "Login page is not displayed."

    # Step 2: Enter unregistered email address
    email_entered = login_page.enter_email(test_email)
    assert email_entered, f"Email '{test_email}' was not accepted for submission."

    # Step 3: Enter any password
    password_entered = login_page.enter_password(test_password)
    assert password_entered, "Password was not masked and accepted."

    # Step 4: Click on the Login button
    login_page.click_login()

    # Step 5: Verify error message displayed: 'Invalid email or password'
    error_displayed = login_page.is_error_message_displayed(expected_error)
    assert error_displayed, f"Expected error message '{expected_error}' not displayed."

    # Step 6: Verify user remains on login page
    user_stays = login_page.verify_user_stays_on_login_page()
    assert user_stays, "User is not authenticated and does not stay on login page."

    # If all assertions pass, the test is successful.
