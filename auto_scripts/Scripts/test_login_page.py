# Selenium Automation Test Script for TC_LOGIN_001
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage
import time

# Test Data
LOGIN_URL = "https://app.example.com/login"
VALID_EMAIL = "testuser@example.com"
VALID_PASSWORD = "ValidPass123!"

@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_TC_LOGIN_001_valid_login(driver):
    """
    Test Case: TC_LOGIN_001 - Valid Login
    Steps:
    1. Navigate to the login page
    2. Enter valid registered email
    3. Enter correct password
    4. Click on the Login button
    5. Verify user session is created
    """
    login_page = LoginPage(driver)

    # Step 1: Navigate to the login page
    is_login_page = login_page.navigate_to_login()
    assert is_login_page, "Step 1 Failed: Login page is not displayed with email and password fields."

    # Step 2: Enter valid registered email
    email_accepted = login_page.enter_email(VALID_EMAIL)
    assert email_accepted, f"Step 2 Failed: Email '{VALID_EMAIL}' was not accepted or displayed in the field."

    # Step 3: Enter correct password
    password_accepted = login_page.enter_password(VALID_PASSWORD)
    assert password_accepted, "Step 3 Failed: Password is not masked or not accepted."

    # Step 4: Click on the Login button
    is_dashboard = login_page.click_login()
    assert is_dashboard, "Step 4 Failed: User is not authenticated or not redirected to dashboard."

    # Step 5: Verify user session is created
    session_created = login_page.verify_user_session()
    assert session_created, "Step 5 Failed: User session token is not generated or user profile is not displayed."

    # Optional: Add a small wait to observe the result in non-headless mode
    # time.sleep(2)
