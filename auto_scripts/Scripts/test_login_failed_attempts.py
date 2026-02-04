# Selenium Test Script for TC_LOGIN_018: Failed Login Attempts and Warning Messages
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage
import time

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_failed_login_attempts_and_warnings(driver):
    """
    Test Case: TC_LOGIN_018
    Description: Test failed login attempts and warning messages on the login page.
    Steps:
    1. Navigate to the login page
    2. Enter valid email and incorrect password, then click Login (Attempts 1-2):
       - Expect standard error message
    3. Attempt login with incorrect password for the 3rd time:
       - Expect warning: 'Invalid credentials. You have 2 more attempts before your account is locked'
    4. Attempt login with incorrect password for the 4th time:
       - Expect warning: 'Invalid credentials. You have 1 more attempt before your account is locked'
    Acceptance Criteria: SCRUM-91
    """
    login_page = LoginPage(driver)
    email = "testuser@example.com"
    wrong_passwords = ["WrongPass1", "WrongPass2", "WrongPass3", "WrongPass4"]

    # Step 1: Navigate to login page
    login_page.go_to_login_page()
    assert login_page.is_login_fields_visible(), "Login fields are not visible on the login page!"

    # Step 2-4: Attempt failed logins and capture error messages
    error_messages = login_page.test_failed_login_attempts_and_warnings(email, wrong_passwords)

    # Step 2: Standard error message for first two attempts
    assert error_messages[0] is not None, "No error message displayed on first failed attempt."
    assert "Invalid credentials" in error_messages[0], f"Unexpected error on 1st attempt: {error_messages[0]}"
    assert error_messages[1] is not None, "No error message displayed on second failed attempt."
    assert "Invalid credentials" in error_messages[1], f"Unexpected error on 2nd attempt: {error_messages[1]}"

    # Step 3: Warning message after third attempt
    assert error_messages[2] is not None, "No error message displayed on third failed attempt."
    assert "Invalid credentials. You have 2 more attempts before your account is locked" in error_messages[2], \
        f"Expected warning not found on 3rd attempt: {error_messages[2]}"

    # Step 4: Warning message after fourth attempt
    assert error_messages[3] is not None, "No error message displayed on fourth failed attempt."
    assert "Invalid credentials. You have 1 more attempt before your account is locked" in error_messages[3], \
        f"Expected warning not found on 4th attempt: {error_messages[3]}"

    # Optionally, print error messages for traceability
    for idx, msg in enumerate(error_messages, start=1):
        print(f"Attempt {idx} error message: {msg}")
