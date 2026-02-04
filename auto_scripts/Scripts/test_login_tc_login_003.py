# Selenium Test Script for TC_LOGIN_003
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_with_incorrect_password_tc_login_003(driver):
    """
    Test Case ID: 119
    Description: Test login with valid email and incorrect password (TC_LOGIN_003)
    Acceptance Criteria: SCRUM-91
    Steps:
        1. Navigate to login page
        2. Enter valid email address
        3. Enter incorrect password
        4. Click on the Login button
        5. Assert error message 'Invalid email or password' is displayed and user remains on login page
    """
    # Test Data
    login_url = "https://app.example.com/login"
    email = "testuser@example.com"
    wrong_password = "WrongPassword123"

    login_page = LoginPage(driver)

    # Step 1: Navigate to the login page
    login_page.go_to_login_page()
    assert driver.current_url.startswith(login_url), f"Expected URL to start with {login_url}, got {driver.current_url}"
    assert login_page.is_login_fields_visible(), "Login fields are not visible on the page."

    # Step 2: Enter valid email address
    assert login_page.enter_email(email), f"Email '{email}' was not entered correctly."

    # Step 3: Enter incorrect password
    assert login_page.enter_password(wrong_password), "Password field is not masked or not entered correctly."

    # Step 4: Click on the Login button
    login_page.click_login()

    # Step 5: Assert error message and user remains on login page
    assert login_page.is_error_message_displayed("Invalid email or password"), "Error message 'Invalid email or password' not displayed."
    assert driver.current_url.startswith(login_url), f"User did not remain on login page. Current URL: {driver.current_url}"
