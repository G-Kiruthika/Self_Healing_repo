'''
Test Script for TC-LOGIN-009: Login with Extremely Long Password
PageClass: LoginPage (auto_scripts/Pages/LoginPage.py)
Traceability:
- TestCase ID: 236
- TestCase Description: Test Case TC-LOGIN-009
- Covered Steps: 1-4
- Related PageClass Method: tc_login_009_extremely_long_password_login

Author: Automation Agent
Standard: Enterprise Selenium Python with Pytest
'''

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage

# Test Data
LOGIN_URL = "https://ecommerce.example.com/login"
VALID_EMAIL = "testuser@example.com"
EXTREMELY_LONG_PASSWORD = (
    "VeryLongPassword" * 100
)  # 1600 characters

@pytest.fixture(scope="function")
def driver():
    # Setup: Chrome headless for CI/CD compatibility
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_tc_login_009_extremely_long_password(driver):
    """
    TC-LOGIN-009: Attempt login with extremely long password.
    Steps:
        1. Navigate to login page.
        2. Enter valid email.
        3. Enter extremely long password.
        4. Click Login and verify error/validation.
    Acceptance Criteria:
        - System truncates input or shows validation error.
        - Error message is displayed or login fails gracefully.
        - User remains unauthenticated (still on login page).
    """
    page = LoginPage(driver)

    # Step 1: Navigate to login page
    driver.get(LOGIN_URL)
    assert driver.current_url == LOGIN_URL, "Login page URL mismatch."

    # Step 2 & 3: Enter valid email and extremely long password
    # Step 4: Click Login and verify
    result = page.tc_login_009_extremely_long_password_login(VALID_EMAIL, EXTREMELY_LONG_PASSWORD)
    assert result is True, (
        "TC-LOGIN-009 failed: System did not show validation error or failed gracefully with extremely long password."
    )

    # Additional checks for traceability
    # Ensure error message or validation error is present
    error_message = None
    validation_message = None
    try:
        error_elem = driver.find_element_by_css_selector("div.alert-danger")
        if error_elem.is_displayed():
            error_message = error_elem.text
    except Exception:
        pass
    try:
        validation_elem = driver.find_element_by_css_selector(".invalid-feedback")
        if validation_elem.is_displayed():
            validation_message = validation_elem.text
    except Exception:
        pass
    assert (
        error_message or validation_message
    ), "No error or validation message displayed for extremely long password."

    # Ensure user is not authenticated
    assert driver.current_url == LOGIN_URL, "User was redirected away from login page after invalid login attempt."
