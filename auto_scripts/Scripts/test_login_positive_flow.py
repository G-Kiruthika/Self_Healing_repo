# test_login_positive_flow.py
# Test Script for TC-LOGIN-001: Positive login scenario
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time

from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope='function')
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_tc_login_001_valid_login_flow(driver):
    """
    Test Case ID: TC-LOGIN-001
    Description: Positive login scenario for valid registered user
    Steps:
    1. Navigate to the e-commerce website login page
    2. Enter valid registered email address in the email field
    3. Enter correct password in the password field
    4. Click on the Login button
    5. Verify user is successfully authenticated and redirected to the dashboard/home page
    6. Verify user session is established (user name in header, session cookie set)
    """
    # Test Data
    login_url = "https://ecommerce.example.com/login"
    valid_email = "testuser@example.com"
    valid_password = "ValidPass123!"
    session_cookie_name = "sessionid"

    login_page = LoginPage(driver)

    # Step 1: Navigate to login page
    driver.get(login_url)
    assert login_page.is_login_page_displayed(), "Login page is not displayed correctly."

    # Step 2: Enter valid registered email
    assert login_page.enter_email(valid_email), f"Email '{valid_email}' was not accepted or not displayed in the field."

    # Step 3: Enter correct password (should be masked)
    assert login_page.enter_password(valid_password), "Password is not masked or not accepted."

    # Step 4: Click on the Login button
    login_page.click_login()

    # Step 5: Wait for dashboard/home page
    try:
        dashboard_header = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(LoginPage.DASHBOARD_HEADER)
        )
        user_profile = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(LoginPage.USER_PROFILE_ICON)
        )
    except Exception:
        pytest.fail("Dashboard or user profile icon not visible after login.")

    assert dashboard_header.is_displayed(), "Dashboard header is not visible after login."
    assert user_profile.is_displayed(), "User profile icon is not visible after login."

    # Step 6: Verify user name in header and session cookie is set
    try:
        user_name_elem = driver.find_element(*LoginPage.USER_PROFILE_ICON)
        assert user_name_elem.is_displayed() and user_name_elem.text.strip() != "", "User name is not displayed in header."
    except NoSuchElementException:
        pytest.fail("User profile name element not found after login.")

    cookies = driver.get_cookies()
    session_cookie = next((c for c in cookies if c.get('name') == session_cookie_name and c.get('value')), None)
    assert session_cookie is not None, f"Session cookie '{session_cookie_name}' not set after login."

    # Final assertion: all steps must pass for successful login
    print("TC-LOGIN-001: Positive login scenario passed.")
