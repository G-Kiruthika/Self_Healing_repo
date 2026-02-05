# test_login_empty_fields.py
"""
Automated Selenium test for TC_LOGIN_005: Validation of empty email and password fields during login.

Test Case Reference: TC_LOGIN_005
Test Steps:
1. Navigate to the login page
2. Leave email field empty
3. Leave password field empty
4. Click on the Login button
5. Verify validation errors: 'Email is required' and 'Password is required'
6. Ensure login is prevented and user remains on login page

Author: Automation Agent
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
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

def test_tc_login_005_empty_fields_validation(driver):
    """
    Test for TC_LOGIN_005: Validates empty email and password field submission on login page.
    """
    login_page = LoginPage(driver)

    # Step 1: Navigate to the login page
    login_page.load()
    assert login_page.is_displayed(), "Login page is not displayed"

    # Step 2 & 3: Leave email and password fields empty
    email_elem = driver.find_element(*LoginPage.EMAIL_FIELD)
    password_elem = driver.find_element(*LoginPage.PASSWORD_FIELD)
    email_elem.clear()
    password_elem.clear()

    # Step 4: Click on the Login button
    login_page.click_login()

    # Step 5: Verify validation errors for both fields
    try:
        validation_errors = driver.find_elements_by_css_selector(".invalid-feedback")
        error_texts = [e.text for e in validation_errors if e.is_displayed()]
        assert any("Email is required" in t for t in error_texts), "'Email is required' validation error not displayed"
        assert any("Password is required" in t for t in error_texts), "'Password is required' validation error not displayed"
    except Exception as e:
        pytest.fail(f"Validation error check failed: {e}")

    # Step 6: Ensure login is prevented and user remains on login page
    current_url = driver.current_url
    assert LoginPage.URL in current_url, f"User did not remain on login page, current URL: {current_url}"
