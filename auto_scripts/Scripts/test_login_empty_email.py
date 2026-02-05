# Selenium test script for TC_LOGIN_003: Login with empty email field
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope='module')
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_empty_email(driver):
    """
    Test Case TC_LOGIN_003:
    1. Navigate to the login page
    2. Leave email field empty
    3. Enter valid password
    4. Click on the Login button
    5. Verify login is prevented
    """
    login_page = LoginPage(driver)

    # Step 1: Navigate to the login page
    assert login_page.navigate_to_login(), "Login page is not displayed."

    # Step 2: Leave email field empty
    assert login_page.leave_email_empty(), "Email field is not empty."

    # Step 3: Enter valid password
    valid_password = "ValidPass123!"
    assert login_page.enter_valid_password(valid_password), "Password is not masked or not accepted."

    # Step 4: Click on the Login button and check for validation error
    assert login_page.click_login_and_check_validation_error(), "Validation error 'Email is required' was not displayed."

    # Step 5: Verify login is prevented and user remains on login page
    assert login_page.verify_login_prevented(), "User was able to proceed with login or did not remain on login page."
