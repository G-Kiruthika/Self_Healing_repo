# Selenium Test Script for TC_LOGIN_002: Login with Remember Me
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage
import time

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_with_valid_credentials_and_remember_me(driver):
    """
    Test Case ID: TC_LOGIN_002
    Description: End-to-end login workflow with valid credentials and Remember Me checked.
    Steps:
        1. Navigate to the login page
        2. Enter valid username
        3. Enter valid password
        4. Check the Remember Me checkbox
        5. Click on the Login button
    Expected:
        - Login page is displayed with username, password fields and Remember Me checkbox
        - Username and password are entered successfully, password is masked
        - Remember Me checkbox is selected
        - User is authenticated, redirected to dashboard, and session is persisted
    """
    login_page = LoginPage(driver)
    EMAIL = "testuser@example.com"
    PASSWORD = "Test@1234"

    # Step 1: Navigate to the login page
    login_page.go_to_login_page()
    assert login_page.is_login_fields_visible(), "Login fields (email, password) not visible."

    # Step 2: Enter valid username
    assert login_page.enter_email(EMAIL), f"Email '{EMAIL}' was not entered correctly."

    # Step 3: Enter valid password
    assert login_page.enter_password(PASSWORD), "Password was not entered or not masked correctly."

    # Step 4: Check the Remember Me checkbox
    assert login_page.check_remember_me(), "Remember Me checkbox was not selected."

    # Step 5: Click on the Login button
    login_page.click_login()
    time.sleep(2)  # Wait for redirection and session creation

    # Expected: User is authenticated, redirected to dashboard, and session is persisted
    assert login_page.is_redirected_to_dashboard(), "User was not redirected to dashboard."
    assert login_page.is_session_token_created(), "Session token was not created or user profile not visible."
