# Selenium Test Script for TC_SCRUM-74_002: Login with valid username and invalid password
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import AssertionError
import time
from auto_scripts.Pages.LoginPage import LoginPage

# Test Data for TC_SCRUM-74_002
test_data = {
    "valid_email": "testuser@example.com",
    "invalid_password": "WrongPassword123"
}

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1920, 1080)
    yield driver
    driver.quit()

@pytest.mark.tcid("TC_SCRUM-74_002")
def test_login_valid_username_invalid_password(driver):
    """
    TC_SCRUM-74_002: Attempt login with valid registered username and incorrect password, expect error and remain on login page.
    Steps:
    1. Navigate to the login page [Test Data: URL: https://application.com/login] [Acceptance Criteria: AC-002]
    2. Enter valid registered username in the username field [Test Data: Username: testuser@example.com] [Acceptance Criteria: AC-002]
    3. Enter incorrect password in the password field [Test Data: Password: WrongPassword123] [Acceptance Criteria: AC-002]
    4. Click on the Login button [Test Data: Button: Login] [Acceptance Criteria: AC-002]
    5. Verify error message is displayed: 'Invalid username or password' and user remains on login page
    """
    login_page = LoginPage(driver)
    result = login_page.login_valid_username_invalid_password(
        valid_email=test_data["valid_email"],
        invalid_password=test_data["invalid_password"]
    )
    assert result is True, "Login with valid username and invalid password did not behave as expected."
    # Traceability: Test Case ID TC_SCRUM-74_002
