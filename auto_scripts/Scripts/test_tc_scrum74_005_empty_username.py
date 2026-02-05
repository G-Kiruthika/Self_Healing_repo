# test_tc_scrum74_005_empty_username.py
"""
Automated Selenium Test for TC_SCRUM74_005: Login Attempt with Empty Username

Test Steps:
1. Navigate to the login page [Test Data: URL: https://app.example.com/login]
2. Leave email/username field empty
3. Enter valid password [Test Data: Password: ValidPass123!]
4. Click on the Login button
5. Validation error displayed: 'Email/Username is required'

Traceability:
- PageClass: LoginPage (auto_scripts/Pages/LoginPage.py)
- TestCaseId: 197 / TC_SCRUM74_005
- Author: AutomationBot
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1280, 900)
    yield driver
    driver.quit()

def test_tc_scrum74_005_empty_username(driver):
    """
    Test Case TC_SCRUM74_005: Login Attempt with Empty Username
    """
    login_page = LoginPage(driver)
    # Step 1: Navigate to the login page
    login_page.load()
    assert login_page.is_displayed(), "Login page is not displayed (Step 1)"

    # Step 2: Leave email/username field empty
    email_elem = driver.find_element(*LoginPage.EMAIL_FIELD)
    email_elem.clear()
    assert email_elem.get_attribute('value') == '', "Email/username field is not empty (Step 2)"

    # Step 3: Enter valid password
    valid_password = "ValidPass123!"
    login_page.enter_password(valid_password)
    password_elem = driver.find_element(*LoginPage.PASSWORD_FIELD)
    # Password should be masked (type='password')
    assert password_elem.get_attribute('type') == 'password', "Password field is not masked (Step 3)"

    # Step 4: Click on the Login button
    login_page.click_login()

    # Step 5: Assert validation error is displayed: 'Email/Username is required'
    validation_error = login_page.get_validation_error()
    assert validation_error is not None, "Validation error not displayed for empty username (Step 5)"
    assert ("Email" in validation_error or "Username" in validation_error), \
        f"Expected 'Email/Username is required' validation error, got: {validation_error} (Step 5)"

    # Ensure user remains on login page
    current_url = driver.current_url
    assert "login" in current_url, f"User did not remain on login page, current URL: {current_url}"

    # Optionally, check if the username field is visually highlighted
    assert login_page.is_username_field_highlighted(), "Username field is not visually highlighted after validation error"
