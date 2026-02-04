# Selenium Automation Test Script for TC_LOGIN_001 (auto-generated)
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage
import time

@pytest.fixture(scope='module')
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_TC_LOGIN_001_successful_login(driver):
    """
    Test Case TC_LOGIN_001: End-to-end login workflow with valid credentials.
    Steps:
    1. Navigate to the login page
    2. Enter valid email address in the email field
    3. Enter valid password in the password field
    4. Click on the Login button
    5. Verify user is logged in (dashboard is displayed with user profile information)
    Acceptance Criteria: AC_001
    Traceability: PageClass=LoginPage, testCaseId=116
    """
    # Test Data
    email = "testuser@example.com"
    password = "ValidPass123!"

    login_page = LoginPage(driver)
    # Step 1: Navigate to the login page
    login_page.go_to_login_page()
    assert driver.current_url == LoginPage.LOGIN_URL, f"Did not navigate to login page: {driver.current_url}"
    assert login_page.is_login_fields_visible(), "Login fields are not visible on the login page."

    # Step 2: Enter valid email address
    assert login_page.enter_email(email), f"Failed to enter email: {email}"
    entered_email = driver.find_element(*LoginPage.EMAIL_FIELD).get_attribute("value")
    assert entered_email == email, f"Email field value mismatch: {entered_email}"

    # Step 3: Enter valid password
    assert login_page.enter_password(password), "Failed to enter password or password is not masked."
    entered_type = driver.find_element(*LoginPage.PASSWORD_FIELD).get_attribute("type")
    assert entered_type == "password", f"Password field is not masked: {entered_type}"

    # Step 4: Click on the Login button
    login_page.click_login()
    time.sleep(2)  # Wait for possible redirect

    # Step 5: Verify user is logged in and redirected to dashboard
    assert login_page.is_redirected_to_dashboard(), "User was not redirected to dashboard after login."
    assert login_page.is_session_token_created(), "Session token was not created or user profile not visible."
    dashboard_header = driver.find_element(*LoginPage.DASHBOARD_HEADER)
    user_icon = driver.find_element(*LoginPage.USER_PROFILE_ICON)
    assert dashboard_header.is_displayed(), "Dashboard header is not displayed!"
    assert user_icon.is_displayed(), "User profile icon is not displayed!"
    print("TC_LOGIN_001: Login workflow completed successfully.")
