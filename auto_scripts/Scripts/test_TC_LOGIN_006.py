# Test Script for TC_LOGIN_006: Login with empty email and empty password
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
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_with_empty_email_and_empty_password(driver):
    """
    Test Case TC_LOGIN_006
    Steps:
    1. Navigate to the login page
    2. Leave both email and password fields empty
    3. Click on the Login button
    Expected:
    - Validation errors 'Email is required' and 'Password is required' are displayed
    - User remains on the login page
    """
    login_page = LoginPage(driver)
    result = login_page.login_with_empty_email_and_empty_password()
    assert result, (
        "Validation errors for both fields should be displayed and user should remain on the login page. "
        "Check that selectors and error messages have not changed."
    )
