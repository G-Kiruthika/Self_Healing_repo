# Selenium Python Test Script for TC_SCRUM-74_003
import pytest
from selenium import webdriver
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope='function')
def driver():
    # Setup: Instantiate Chrome WebDriver (adjust as needed)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_special_characters_username(driver):
    """
    TC_SCRUM-74_003: Login with username containing special characters (dots, underscores, hyphens) and verify successful authentication and dashboard redirection.
    Steps:
    1. Navigate to the login page [Test Data: URL: https://application.com/login]
    2. Enter valid username containing special characters (dots, underscores, hyphens) [Test Data: Username: test.user_name-123@example.com]
    3. Enter valid password in the password field [Test Data: Password: ValidPass123!]
    4. Click on the Login button
    5. Verify successful login and redirection [Expected: User dashboard displayed]
    """
    login_page = LoginPage(driver)
    special_username = "test.user_name-123@example.com"
    valid_password = "ValidPass123!"
    result = login_page.login_special_characters_username(special_username, valid_password)
    assert result, "Login with special characters in username failed or did not redirect to dashboard!"
