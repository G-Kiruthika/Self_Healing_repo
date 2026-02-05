# Test Script for TC_SCRUM-74_003: Login with special characters in username
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage
import time

@pytest.fixture(scope="module")
def driver():
    # Configure Chrome options for headless execution if needed
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_with_special_characters_username(driver):
    """
    TC_SCRUM-74_003: Login with username containing special characters (dots, underscores, hyphens), verify acceptance and successful authentication.
    Steps:
    1. Navigate to the login page [Test Data: URL: https://application.com/login] [Acceptance Criteria: AC-001]
    2. Enter valid username containing special characters (dots, underscores, hyphens) [Test Data: Username: test.user_name-123@example.com] [Acceptance Criteria: AC-001]
    3. Enter valid password in the password field [Test Data: Password: ValidPass123!] [Acceptance Criteria: AC-001]
    4. Click on the Login button [Test Data: Button: Login] [Acceptance Criteria: AC-001]
    5. Verify successful login and redirection [Test Data: Expected: User dashboard displayed] [Acceptance Criteria: AC-001]
    """
    login_page = LoginPage(driver)
    special_username = "test.user_name-123@example.com"
    password = "ValidPass123!"
    # Call the PageClass method which contains all assertions and logic
    assert login_page.login_special_characters_username(special_username, password) is True
