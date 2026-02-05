# Test Script for TC_SCRUM74_005: Email/Username Empty Validation on Login
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope='module')
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_tc_scrum74_005_email_username_required(driver):
    """
    Test Case TC_SCRUM74_005:
    1. Navigate to the login page
    2. Leave email/username field empty
    3. Enter valid password
    4. Click on the Login button
    5. Validation error displayed: 'Email/Username is required'
    """
    login_page = LoginPage(driver)

    # Step 1: Navigate to login page
    assert login_page.navigate_to_login(), "Login page did not load correctly."

    # Step 2: Leave email/username field empty
    assert login_page.leave_email_field_empty(), "Email field is not empty after clearing."

    # Step 3: Enter valid password
    valid_password = "ValidPass123!"
    assert login_page.enter_valid_password(valid_password), "Password is not accepted or masked."

    # Step 4: Click Login button
    login_page.click_login_button()

    # Step 5: Assert validation error is displayed
    assert login_page.is_validation_error_displayed("Email/Username is required"), (
        "Expected validation error 'Email/Username is required' was not displayed."
    )
