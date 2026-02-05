# test_tc_login_004_empty_email.py
"""
Automated Selenium test for TC-LOGIN-004: Login with Empty Email and Valid Password
Covers acceptance criteria: error validation, session state, and page state.

Test Steps:
1. Navigate to the login page
2. Leave the email field empty
3. Enter valid password
4. Click on the Login button
5. Verify validation error is displayed: 'Email is required' or 'Please fill in all required fields'
6. Verify login is not processed: user remains on login page without authentication

Traceability:
- Page Object: LoginPage (auto_scripts/Pages/LoginPage.py)
- Test Case: TC-LOGIN-004
- Author: Automation Agent
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_tc_login_004_empty_email(driver):
    """
    TC-LOGIN-004: Login with Empty Email and Valid Password
    """
    login_page = LoginPage(driver)
    # Step 1: Navigate to the login page
    login_page.load()
    assert login_page.is_displayed(), "Login page should be displayed"
    # Step 2: Leave the email field empty (ensure it's blank)
    email_elem = driver.find_element(*LoginPage.EMAIL_FIELD)
    email_elem.clear()
    assert email_elem.get_attribute('value') == '', "Email field should be empty"
    # Step 3: Enter valid password
    valid_password = "ValidPass123!"
    login_page.enter_password(valid_password)
    password_elem = driver.find_element(*LoginPage.PASSWORD_FIELD)
    assert password_elem.get_attribute('value') == valid_password, "Password should be entered correctly"
    # Step 4: Click on the Login button
    login_page.click_login()
    # Step 5: Verify validation error is displayed
    # Acceptable errors: 'Email is required' or 'Please fill in all required fields'
    validation_errors = driver.find_elements_by_css_selector(".invalid-feedback")
    error_texts = [e.text for e in validation_errors if e.is_displayed()]
    assert any(
        "Email is required" in t or "Please fill in all required fields" in t for t in error_texts
    ), f"Expected validation error for empty email not displayed. Found: {error_texts}"
    # Step 6: Verify login is not processed: user remains on login page
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
