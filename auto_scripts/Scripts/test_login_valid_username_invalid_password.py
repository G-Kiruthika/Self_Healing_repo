# Test Script for TC_SCRUM-74_002: Valid Username, Invalid Password (Login Negative Scenario)
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_login_valid_username_invalid_password(driver):
    """
    TC_SCRUM-74_002: Attempt login with valid registered username and incorrect password, expect error and remain on login page.
    Steps:
    1. Navigate to the login page [Test Data: URL: https://application.com/login]
    2. Enter valid registered username in the username field [Test Data: Username: testuser@example.com]
    3. Enter incorrect password in the password field [Test Data: Password: WrongPassword123]
    4. Click on the Login button [Test Data: Button: Login]
    5. Verify error message is displayed: 'Invalid username or password' and user remains on login page
    """
    login_page = LoginPage(driver)
    valid_email = "testuser@example.com"
    invalid_password = "WrongPassword123"
    assert login_page.login_valid_username_invalid_password(valid_email, invalid_password)
