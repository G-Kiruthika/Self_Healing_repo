'''
Test Script for TC-LOGIN-014: Login attempt with locked account
This script automates and validates the following scenario:
- Navigate to login page
- Enter credentials for a locked user
- Click Login
- Assert error message and that user is not authenticated
Traceability: TC-LOGIN-014
'''
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
import time
import sys
import os

# Ensure Pages package is importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Pages.LoginPage import LoginPage

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

def test_tc_login_014_locked_account(driver):
    """
    TC-LOGIN-014: Login attempt with locked account
    Steps:
        1. Navigate to the login page
        2. Enter email of a locked account
        3. Enter correct password for the locked account
        4. Click on the Login button
        5. Verify error message: 'Your account has been locked. Please contact support.'
        6. Verify user is not authenticated (remains on login page)
    """
    login_page = LoginPage(driver)
    email = 'lockeduser@example.com'
    password = 'CorrectPassword123!'

    # Step 1: Navigate to login page
    driver.get('https://ecommerce.example.com/login')
    assert 'login' in driver.current_url.lower(), 'Login page did not load as expected.'

    # Step 2 & 3: Enter credentials
    try:
        email_field = login_page.wait.until(
            lambda d: d.find_element(*login_page.EMAIL_FIELD)
        )
        email_field.clear()
        email_field.send_keys(email)
        password_field = login_page.wait.until(
            lambda d: d.find_element(*login_page.PASSWORD_FIELD)
        )
        password_field.clear()
        password_field.send_keys(password)
    except Exception as e:
        pytest.fail(f'Failed to locate/enter credentials: {e}')

    # Step 4: Click Login
    try:
        login_button = login_page.wait.until(
            lambda d: d.find_element(*login_page.LOGIN_SUBMIT_BUTTON)
        )
        login_button.click()
    except Exception as e:
        pytest.fail(f'Failed to click login button: {e}')

    # Step 5: Assert error message is displayed
    try:
        error_elem = login_page.wait.until(
            lambda d: d.find_element(*login_page.ERROR_MESSAGE)
        )
        assert error_elem.is_displayed(), 'Error message not displayed for locked account.'
        assert 'locked' in error_elem.text.lower(), \
            f"Expected locked account message, got: {error_elem.text}"
        assert 'contact support' in error_elem.text.lower(), \
            f"Expected contact support message, got: {error_elem.text}"
    except Exception as e:
        pytest.fail(f'Error message for locked account not found or incorrect: {e}')

    # Step 6: Assert user is not authenticated (remains on login page)
    assert driver.current_url == 'https://ecommerce.example.com/login', \
        f"User was redirected from login page: {driver.current_url}"
    # Ensure dashboard header/user icon are not present
    dashboard_present = False
    user_icon_present = False
    try:
        driver.find_element(*login_page.DASHBOARD_HEADER)
        dashboard_present = True
    except Exception:
        dashboard_present = False
    try:
        driver.find_element(*login_page.USER_PROFILE_ICON)
        user_icon_present = True
    except Exception:
        user_icon_present = False
    assert not dashboard_present, 'Dashboard header should not be present for locked account.'
    assert not user_icon_present, 'User icon should not be present for locked account.'
