# Selenium Test Script for TC_LOGIN_002: Login with Incorrect Password
# Traceability: TC_LOGIN_002 | auto_scripts/Pages/LoginPage.py
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
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

def test_login_with_incorrect_password(driver):
    """
    Test Case: TC_LOGIN_002
    Description: Attempt login with valid email and incorrect password, verify error and that user remains on login page.
    Steps:
      1. Navigate to login page
      2. Enter valid registered email
      3. Enter incorrect password
      4. Click Login button
      5. Verify error message and that user is not authenticated
    Acceptance Criteria: As per test case definition
    """
    EMAIL = "testuser@example.com"
    INCORRECT_PASSWORD = "WrongPass456!"
    EXPECTED_ERROR = "Invalid email or password"

    # Step 1: Navigate to login page
    login_page = LoginPage(driver)
    assert login_page.navigate_to_login(), "Login page should be displayed (Step 1)"

    # Step 2: Enter valid registered email
    assert login_page.enter_email(EMAIL), f"Email '{EMAIL}' should be accepted (Step 2)"

    # Step 3: Enter incorrect password
    assert login_page.enter_incorrect_password(INCORRECT_PASSWORD), "Password should be masked and accepted for submission (Step 3)"

    # Step 4: Click Login and verify error message
    assert login_page.click_login_and_check_error(), f"Error message '{EXPECTED_ERROR}' should be displayed (Step 4)"

    # Step 5: Verify user remains on login page (not authenticated)
    assert login_page.verify_user_stays_on_login_page(), "User should remain on login page after failed login (Step 5)"
