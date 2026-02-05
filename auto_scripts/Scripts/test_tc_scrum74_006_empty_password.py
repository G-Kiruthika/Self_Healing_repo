# test_tc_scrum74_006_empty_password.py
"""
Automated Selenium test for TC_SCRUM74_006: Login with Valid Email and Empty Password
- Validates error message 'Password is required' is shown when attempting login with empty password.
- Ensures user remains on login page and no authentication is performed.

Traceability:
- Page Object: LoginPage (auto_scripts/Pages/LoginPage.py)
- Test Case ID: 199 / TC_SCRUM74_006
- Acceptance Criteria: AC_005
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
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_tc_scrum74_006_empty_password(driver):
    """
    TC_SCRUM74_006 Steps:
    1. Navigate to the login page
    2. Enter valid email (testuser@example.com)
    3. Leave password field empty
    4. Click on the Login button
    5. Validate error message: 'Password is required'
    """
    login_page = LoginPage(driver)
    # Step 1: Navigate to login page
    login_page.load()
    assert login_page.is_displayed(), "Login page is not displayed"

    # Step 2: Enter valid email
    valid_email = "testuser@example.com"
    login_page.enter_email(valid_email)
    email_field_value = driver.find_element(*LoginPage.EMAIL_FIELD).get_attribute("value")
    assert email_field_value == valid_email, f"Email field value mismatch: expected '{valid_email}', got '{email_field_value}'"

    # Step 3: Leave password field empty
    password_elem = driver.find_element(*LoginPage.PASSWORD_FIELD)
    password_elem.clear()
    password_field_value = password_elem.get_attribute("value")
    assert password_field_value == "", "Password field is not empty before login attempt"

    # Step 4: Click on the Login button
    login_page.click_login()

    # Step 5: Validate error message
    validation_errors = driver.find_elements_by_css_selector(".invalid-feedback")
    error_texts = [e.text for e in validation_errors if e.is_displayed()]
    assert any("Password is required" in t for t in error_texts), f"'Password is required' validation error not displayed. Found: {error_texts}"

    # Ensure user remains on login page
    current_url = driver.current_url
    assert LoginPage.URL in current_url or "app.example.com/login" in current_url, f"User did not remain on login page, current URL: {current_url}"
