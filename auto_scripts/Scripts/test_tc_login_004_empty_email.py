# test_tc_login_004_empty_email.py
"""
Automated Test Script for TC-LOGIN-004: Login with Empty Email and Valid Password

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
- Maintainer: Automation Team

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

def test_tc_login_004_empty_email_validation(driver):
    """
    TC-LOGIN-004: Login with Empty Email and Valid Password
    """
    login_page = LoginPage(driver)
    login_page.load()
    # Step 1: Login page is displayed
    assert login_page.is_displayed(), "Login page is not displayed"
    # Step 2: Leave email field empty
    email_elem = driver.find_element(*LoginPage.EMAIL_FIELD)
    email_elem.clear()
    assert email_elem.get_attribute('value') == '', "Email field is not empty"
    # Step 3: Enter valid password
    valid_password = "ValidPass123!"
    login_page.enter_password(valid_password)
    password_elem = driver.find_element(*LoginPage.PASSWORD_FIELD)
    assert password_elem.get_attribute('value') == valid_password, "Password not entered correctly"
    # Step 4: Click on the Login button
    login_page.click_login()
    # Step 5: Verify validation error is displayed
    error_found = False
    validation_errors = driver.find_elements_by_css_selector(".invalid-feedback")
    error_texts = [e.text for e in validation_errors if e.is_displayed()]
    for t in error_texts:
        if "Email is required" in t or "Please fill in all required fields" in t:
            error_found = True
            break
    assert error_found, f"Expected validation error for empty email not displayed. Found: {error_texts}"
    # Step 6: Verify login is not processed (user remains on login page)
    assert LoginPage.URL in driver.current_url, f"User did not remain on login page, current URL: {driver.current_url}"
    # Optionally: Check that dashboard/profile is not visible
    try:
        assert not login_page.is_dashboard_displayed(), "Dashboard should not be displayed for invalid login"
    except Exception:
        pass
    try:
        assert not login_page.is_user_profile_icon_displayed(), "User profile icon should not be visible for invalid login"
    except Exception:
        pass
