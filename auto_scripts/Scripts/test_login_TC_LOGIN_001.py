# Selenium Automation Test Script for TC_LOGIN_001
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_TC_LOGIN_001_valid_login(driver):
    """
    Test Case ID: TC_LOGIN_001
    Description: Valid login with registered email and correct password, verify session and dashboard.
    Steps:
    1. Navigate to the login page
    2. Enter valid registered email
    3. Enter correct password
    4. Click on the Login button
    5. Verify user is authenticated and redirected to dashboard
    6. Verify user session is created and user profile is displayed
    """
    # Test Data
    valid_email = "testuser@example.com"
    valid_password = "ValidPass123!"

    login_page = LoginPage(driver)

    # Step 1: Navigate to the login page
    assert login_page.navigate_to_login(), "Login page should be displayed with email and password fields."

    # Step 2: Enter valid registered email
    assert login_page.enter_email(valid_email), f"Email '{valid_email}' should be accepted and displayed in the field."

    # Step 3: Enter correct password
    assert login_page.enter_password(valid_password), "Password should be masked and accepted."

    # Step 4: Click on the Login button
    assert login_page.click_login(), "User should be redirected to dashboard after successful login."

    # Step 5: Verify dashboard and profile
    assert login_page.is_dashboard_displayed(), "Dashboard and user profile should be visible after login."

    # Step 6: Verify user session is created
    assert login_page.verify_user_session(), "User session token should be generated and user profile displayed."
