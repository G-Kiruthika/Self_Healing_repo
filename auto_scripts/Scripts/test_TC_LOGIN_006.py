# Selenium Test Script for TC_LOGIN_006: Empty Email and Password Validation
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope='function')
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_TC_LOGIN_006_empty_email_and_empty_password(driver):
    """
    TC_LOGIN_006: Attempt login with both email and password fields empty; verify validation errors for both fields are displayed.
    Steps:
    1. Navigate to the login page
    2. Leave both email and password fields empty
    3. Click Login button
    4. Verify validation errors 'Email is required' and 'Password is required' are displayed
    5. User remains on login page and is not authenticated
    """
    login_page = LoginPage(driver)
    result = login_page.login_with_empty_email_and_empty_password()
    assert result is True, "Validation errors for empty email and password were not displayed as expected."
    # Additional assertion: user remains on login page
    assert driver.current_url == login_page.LOGIN_URL, "User is not on login page after failed login!"
