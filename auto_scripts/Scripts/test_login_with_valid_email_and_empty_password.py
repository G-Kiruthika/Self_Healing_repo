# Selenium Test Script for TC_LOGIN_005: Login with valid email and empty password
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import AssertionError
from auto_scripts.Pages.LoginPage import LoginPage

# Test Data for TC_LOGIN_005
VALID_EMAIL = "testuser@example.com"
EMPTY_PASSWORD = ""

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    # You may set the ChromeDriver path as needed
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_with_valid_email_and_empty_password(driver):
    """
    TC_LOGIN_005: Attempt login with valid email and empty password; verify validation error for password is displayed.
    Steps:
        1. Navigate to the login page
        2. Enter valid email address
        3. Leave password field empty
        4. Click Login button
        5. Verify validation error 'Password is required' is displayed below password field
    Acceptance Criteria: SCRUM-91
    """
    login_page = LoginPage(driver)
    try:
        result = login_page.login_with_valid_email_and_empty_password(VALID_EMAIL)
        assert result is True, "TC_LOGIN_005 failed: The validation error was not correctly detected."
    except AssertionError as e:
        pytest.fail(str(e))
