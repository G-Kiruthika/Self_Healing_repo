# test_tc_scrum74_006_empty_password.py
"""
Automated Selenium test for TC_SCRUM74_006: Login with valid email and empty password.
Ensures 'Password is required' validation error is displayed and user remains on login page.

Test Case Reference: 199 / TC_SCRUM74_006
Author: Automation Agent
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
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_tc_scrum74_006_empty_password(driver):
    """
    Steps:
    1. Navigate to the login page [Test Data: URL: https://app.example.com/login]
    2. Enter valid email [Test Data: Email: testuser@example.com]
    3. Leave password field empty [Test Data: Password: '']
    4. Click on the Login button [Test Data: N/A]
    5. Validation error displayed: 'Password is required'
    """
    login_page = LoginPage(driver)
    # Step 1: Navigate to login page
    login_page.load()
    assert login_page.is_displayed(), "Login page is not displayed"
    # Step 2: Enter valid email
    login_page.enter_email("testuser@example.com")
    # Step 3: Leave password field empty (ensure field is cleared)
    password_elem = driver.find_element(*LoginPage.PASSWORD_FIELD)
    password_elem.clear()
    # Step 4: Click Login
    login_page.click_login()
    # Step 5: Assert validation error
    validation_errors = driver.find_elements_by_css_selector(".invalid-feedback")
    error_texts = [e.text for e in validation_errors if e.is_displayed()]
    assert any("Password is required" in t for t in error_texts), "'Password is required' validation error not displayed"
    # Ensure user remains on login page
    current_url = driver.current_url
    assert "login" in current_url, f"User did not remain on login page, current URL: {current_url}"
