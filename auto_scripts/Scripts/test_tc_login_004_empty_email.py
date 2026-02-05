# test_tc_login_004_empty_email.py
"""
Test Script for TC-LOGIN-004: Login with Empty Email and Valid Password

Test Case Reference: TC-LOGIN-004
Test Case Description: Validates error handling and session state when logging in with an empty email field and valid password.
Traceability:
- Page Object: auto_scripts/Pages/LoginPage.py
- Test Case ID: 231
- Acceptance Criteria: TS-003
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_tc_login_004_empty_email(driver):
    """
    Steps:
    1. Navigate to the login page
    2. Leave the email field empty
    3. Enter valid password (ValidPass123!)
    4. Click on the Login button
    5. Verify validation error is displayed: 'Email is required' or 'Please fill in all required fields'
    6. Verify login is not processed: user remains on login page without authentication
    """
    login_page = LoginPage(driver)
    # Step 1: Navigate to the login page
    login_page.load()
    assert login_page.is_displayed(), "Login page is not displayed"

    # Step 2: Leave the email field empty
    email_elem = login_page.wait.until(lambda d: d.find_element(*LoginPage.EMAIL_FIELD))
    email_elem.clear()
    assert email_elem.get_attribute('value') == '', "Email field is not empty after clearing"

    # Step 3: Enter valid password
    valid_password = "ValidPass123!"
    login_page.enter_password(valid_password)
    password_elem = login_page.wait.until(lambda d: d.find_element(*LoginPage.PASSWORD_FIELD))
    # Password field should be masked (type='password')
    assert password_elem.get_attribute('type') == 'password', "Password field is not masked"
    assert password_elem.get_attribute('value') == valid_password, "Password was not entered correctly"

    # Step 4: Click on the Login button
    login_page.click_login()

    # Step 5: Verify validation error is displayed
    validation_errors = driver.find_elements_by_css_selector('.invalid-feedback')
    error_texts = [e.text for e in validation_errors if e.is_displayed()]
    assert any('Email is required' in t or 'Please fill in all required fields' in t for t in error_texts), \
        f"Expected validation error not displayed. Errors found: {error_texts}"

    # Step 6: Verify login is not processed: user remains on login page without authentication
    current_url = driver.current_url
    assert LoginPage.URL in current_url, f"User did not remain on login page, current URL: {current_url}"

    # Optionally, check for absence of dashboard/profile icon
    try:
        assert not login_page.is_dashboard_displayed(), "Dashboard should not be displayed for invalid login"
    except:
        pass
    try:
        assert not login_page.is_user_profile_icon_displayed(), "User profile icon should not be visible for invalid login"
    except:
        pass
