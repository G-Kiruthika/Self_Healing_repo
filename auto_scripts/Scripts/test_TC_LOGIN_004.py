# Selenium Test Script for TC_LOGIN_004: Login with Empty Password Field
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope='module')
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_empty_password(driver):
    """
    Test Case: TC_LOGIN_004
    Description: Verify that attempting to login with an empty password field displays the correct validation error and prevents login.
    Steps:
      1. Navigate to the login page
      2. Enter valid registered email
      3. Leave password field empty
      4. Click on the Login button
      5. Verify login is prevented and user remains on login page
    Acceptance Criteria: Validation error 'Password is required' is displayed and user is not authenticated.
    """
    login_page = LoginPage(driver)

    # Step 1: Navigate to the login page
    assert login_page.navigate_to_login(), "Login page should be displayed"

    # Step 2: Enter valid registered email
    email = "testuser@example.com"
    assert login_page.enter_email(email), f"Email '{email}' should be accepted in the field"

    # Step 3: Leave password field empty
    assert login_page.leave_password_field_empty(), "Password field should remain empty"

    # Step 4: Click on the Login button
    assert login_page.click_login_with_empty_password(), "Validation error 'Password is required' should be displayed"

    # Step 5: Verify login is prevented and user remains on login page
    assert login_page.verify_login_prevented_for_empty_password(), "User should not be able to proceed and must remain on login page"
