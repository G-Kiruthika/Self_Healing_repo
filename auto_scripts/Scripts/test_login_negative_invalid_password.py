# Selenium Pytest Test Script for TC_LOGIN_003
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

def test_login_with_valid_email_invalid_password(driver):
    """
    Test Case ID: TC_LOGIN_003
    Description: Attempt login with valid email and invalid password; verify error message and user remains on login page.
    Acceptance Criteria: SCRUM-91
    Test Data:
        Email: testuser@example.com
        Password: WrongPassword123
    Steps:
        1. Navigate to the login page
        2. Enter valid email address
        3. Enter incorrect password
        4. Click Login button
        5. Verify error message is displayed: 'Invalid email or password'
        6. Verify user remains on login page (not authenticated)
    """
    login_page = LoginPage(driver)
    result = login_page.login_with_valid_email_invalid_password(
        email="testuser@example.com",
        invalid_password="WrongPassword123"
    )
    assert result, "Login with valid email and invalid password did not behave as expected."
