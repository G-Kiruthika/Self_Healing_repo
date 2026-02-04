# Selenium Test Script for LoginPage TC_LOGIN_001
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage
import time

@pytest.fixture(scope='module')
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_TC_LOGIN_001_successful_login(driver):
    """
    TC_LOGIN_001: End-to-end login workflow with valid credentials.
    Steps:
    1. Navigate to the login page
    2. Enter valid email address in the email field
    3. Enter valid password in the password field
    4. Click on the Login button
    5. Verify user is logged in (dashboard is displayed with user profile information)
    Acceptance Criteria: AC_001
    """
    # Test Data
    email = "testuser@example.com"
    password = "ValidPass123!"

    login_page = LoginPage(driver)
    login_page.go_to_login_page()

    # Step 1: Login page is displayed with email and password fields
    assert login_page.is_login_fields_visible(), "Login fields are not visible on the login page."

    # Step 2: Enter valid email address
    assert login_page.enter_email(email), f"Failed to enter email: {email}"

    # Step 3: Enter valid password
    assert login_page.enter_password(password), "Failed to enter password or password is not masked."

    # Optional: Check 'Remember Me' if required
    # assert login_page.check_remember_me(), "Failed to check 'Remember Me' checkbox."

    # Step 4: Click on the Login button
    login_page.click_login()

    # Step 5: User is successfully authenticated and redirected to dashboard
    assert login_page.is_redirected_to_dashboard(), "User was not redirected to dashboard after login."
    assert login_page.is_session_token_created(), "Session token not created or user profile not visible after login."
    
    # Optionally, print success message
    print("TC_LOGIN_001: Login workflow completed successfully.")
