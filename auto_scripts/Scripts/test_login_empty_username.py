# Test Script for TC_SCRUM-74_004: Login with empty username and valid password
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

def test_login_empty_username_valid_password(driver):
    """
    TC_SCRUM-74_004
    Title: Attempt login with empty username and valid password, expect 'Username is required' error and login is not processed.
    Steps:
    1. Navigate to the login page [Test Data: URL: https://application.com/login]
    2. Leave the username field empty (no input)
    3. Enter valid password in the password field [Test Data: Password: ValidPass123!]
    4. Click on the Login button
    5. Verify validation error message is displayed: 'Username is required' and login is not processed.
    Acceptance Criteria: User is not authenticated, error message is shown, and user remains on login page.
    """
    login_page = LoginPage(driver)
    valid_password = "ValidPass123!"  # Replace with actual valid password if needed
    expected_error = "Username is required"
    result = login_page.login_empty_username_valid_password(password=valid_password, expected_error=expected_error)
    assert result is True, "Test failed: Login with empty username did not behave as expected."
