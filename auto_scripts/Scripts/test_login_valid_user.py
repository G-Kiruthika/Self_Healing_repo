# Selenium Test Script for TC_LOGIN_001: Valid Login
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_valid_user(driver):
    """
    Test Case ID: TC_LOGIN_001
    Description: Validates login with correct credentials and session creation.
    """
    login_page = LoginPage(driver)
    # Step 1: Navigate to login page
    login_page.go_to_login_page()
    # Assert login fields are visible
    assert login_page.is_login_fields_visible(), "Login fields (email & password) are not visible."

    # Step 2: Enter valid email
    email = "testuser@example.com"
    assert login_page.enter_email(email), f"Email field value mismatch after entering: {email}"

    # Step 3: Enter valid password
    password = "ValidPass123!"
    assert login_page.enter_password(password), "Password field is not masked or not accepted."

    # Step 4: Click Login
    login_page.click_login()

    # Step 5: Wait for dashboard redirection
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(LoginPage.DASHBOARD_HEADER)
        )
    except TimeoutException:
        pytest.fail("Dashboard header not visible after login.")
    assert login_page.is_redirected_to_dashboard(), "User is not redirected to dashboard after login."

    # Step 6: Verify session token and user profile
    assert login_page.is_session_token_created(), "Session token not created or user profile not visible after login."

    # Negative test: Ensure no error message is displayed
    assert not login_page.is_error_message_displayed(), "Unexpected error message displayed for valid login."
