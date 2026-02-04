# Selenium Test Script for TC_LOGIN_004: Login with empty email and valid password
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage
import time

@pytest.fixture(scope='module')
def driver():
    options = Options()
    options.add_argument('--headless')  # Comment out if you want to see the browser
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_with_empty_email_and_valid_password(driver):
    """
    TC_LOGIN_004:
    1. Navigate to the login page
    2. Leave email field empty
    3. Enter valid password
    4. Click on the Login button
    5. Assert validation error 'Email is required' is displayed below email field
    """
    login_page = LoginPage(driver)
    # Step 1: Navigate to the login page
    login_page.go_to_login_page()
    assert driver.current_url == LoginPage.LOGIN_URL, "Login page URL mismatch."
    assert login_page.is_login_fields_visible(), "Login fields are not visible."

    # Step 2: Leave email field empty
    entered = login_page.enter_email("")
    assert entered, "Email field was not left empty."

    # Step 3: Enter valid password
    password = "ValidPass123!"
    password_masked = login_page.enter_password(password)
    assert password_masked, "Password field is not masked or password entry failed."

    # Step 4: Click on the Login button
    login_page.click_login()

    # Step 5: Assert validation error 'Email is required' is displayed below email field
    # Allow time for validation message to appear if necessary
    time.sleep(1)
    result = login_page.login_with_empty_email_and_valid_password(password)
    assert result, "Validation error 'Email is required' was not displayed as expected."
