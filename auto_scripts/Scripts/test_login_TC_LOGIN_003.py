# Selenium Automation Test Script for TC_LOGIN_003
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_with_valid_email_invalid_password(driver):
    """
    TC_LOGIN_003: Attempt login with valid email and invalid password; verify error message and user remains on login page.
    Steps:
    1. Navigate to the login page
    2. Enter valid email address
    3. Enter incorrect password
    4. Click Login button
    5. Verify error message is displayed: 'Invalid email or password'
    6. Verify user remains on login page (not authenticated)
    Acceptance Criteria: SCRUM-91
    """
    login_page = LoginPage(driver)
    valid_email = "testuser@example.com"
    invalid_password = "WrongPassword123"

    # Step 1: Navigate to the login page
    login_page.go_to_login_page()
    assert driver.current_url == login_page.LOGIN_URL, "Login page did not load correctly."

    # Step 2: Enter valid email address
    assert login_page.enter_email(valid_email), "Email was not entered correctly."

    # Step 3: Enter incorrect password
    assert login_page.enter_password(invalid_password), "Password was not entered/masked correctly."

    # Step 4: Click Login button
    login_page.click_login()

    # Step 5: Verify error message is displayed: 'Invalid email or password'
    import time
    time.sleep(1)  # Wait for error message
    error_message = login_page.get_error_message()
    assert error_message is not None, "No error message displayed!"
    assert "invalid email or password" in error_message.lower(), f"Unexpected error message: {error_message}"

    # Step 6: Verify user remains on login page (not authenticated)
    assert driver.current_url == login_page.LOGIN_URL, "User is not on login page after failed login!"
