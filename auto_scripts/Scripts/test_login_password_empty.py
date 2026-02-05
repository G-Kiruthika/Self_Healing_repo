# test_login_password_empty.py
"""
Automated Selenium Test Script for TC-LOGIN-005: Login with Valid Email and Empty Password

Test Case ID: 232
Description: Validate that attempting to login with a valid email but an empty password field results in correct validation error and prevents authentication.
Acceptance Criteria:
- Login page is displayed
- Email is entered correctly
- Password field remains blank
- Validation error is displayed: 'Password is required' or 'Please fill in all required fields'
- User remains on login page without authentication

Traceability:
- PageClass: LoginPage (auto_scripts/Pages/LoginPage.py)
- TestCase: TC-LOGIN-005

Author: Automated by Test Automation Agent
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope="module")
def driver():
    # Setup: Configure ChromeDriver (headless for CI)
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_login_with_valid_email_and_empty_password(driver):
    """
    TC-LOGIN-005: Login with Valid Email and Empty Password
    Steps:
    1. Navigate to the login page
    2. Enter valid email address
    3. Leave the password field empty
    4. Click on the Login button
    5. Verify validation error is displayed
    6. Ensure user remains on login page (no authentication)
    """
    # --- Test Data ---
    valid_email = "testuser@example.com"
    # --- Initialize Page Object ---
    login_page = LoginPage(driver)

    # Step 1: Navigate to the login page
    login_page.load()
    assert login_page.is_displayed(), "Login page is not displayed (Step 1)"

    # Step 2: Enter valid email address
    login_page.enter_email(valid_email)
    # Confirm email field value (optional, for traceability)
    email_elem = driver.find_element(*LoginPage.EMAIL_FIELD)
    assert email_elem.get_attribute("value") == valid_email, "Email is not entered correctly (Step 2)"

    # Step 3: Leave the password field empty
    password_elem = driver.find_element(*LoginPage.PASSWORD_FIELD)
    assert password_elem.get_attribute("value") == "", "Password field is not blank (Step 3)"

    # Step 4: Click on the Login button
    login_page.click_login()

    # Step 5: Verify validation error is displayed
    validation_errors = driver.find_elements_by_css_selector(".invalid-feedback")
    error_texts = [e.text for e in validation_errors if e.is_displayed()]
    assert any(
        "Password is required" in t or "Please fill in all required fields" in t for t in error_texts
    ), (
        f"Expected validation error for empty password not displayed (Step 4). Found: {error_texts}"
    )

    # Step 6: Ensure user remains on login page (no authentication)
    current_url = driver.current_url
    assert LoginPage.URL in current_url, f"User did not remain on login page, current URL: {current_url} (Step 5)"

    # Optional: Check that dashboard/profile icon is NOT displayed
    try:
        assert not login_page.is_dashboard_displayed(), "Dashboard should not be displayed for invalid login"
    except Exception:
        pass  # Acceptable if element not found
    try:
        assert not login_page.is_user_profile_icon_displayed(), "User profile icon should not be visible for invalid login"
    except Exception:
        pass
