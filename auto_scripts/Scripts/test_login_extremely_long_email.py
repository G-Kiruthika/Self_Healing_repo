'''
Test Script for TC-LOGIN-008: Login with Extremely Long Email Address
Covers:
- Step-by-step navigation and validation for extremely long email input
- Uses LoginPage PageClass and Selenium best practices
- Asserts: system truncates input, shows validation error, or login fails gracefully
'''

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from auto_scripts.Pages.LoginPage import LoginPage

# Test Data
LONG_EMAIL = (
    "verylongemailaddress" * 12 + "@example.com"
)  # 255+ characters
VALID_PASSWORD = "ValidPass123!"
LOGIN_URL = "https://example-ecommerce.com/login"

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1920, 1080)
    yield driver
    driver.quit()

def test_tc_login_008_extremely_long_email(driver):
    """
    TC-LOGIN-008: Attempt login with extremely long email address
    Steps:
        1. Navigate to login page
        2. Enter extremely long email address
        3. Enter valid password
        4. Click Login
        5. Assert system response: truncation, validation error, or graceful failure
    """
    page = LoginPage(driver)
    # Step 1: Navigate to login page
    driver.get(LOGIN_URL)
    assert driver.current_url.startswith(LOGIN_URL), "Login page did not load."

    # Step 2 & 3: Enter extremely long email and valid password
    result = page.tc_login_008_extremely_long_email_login(LONG_EMAIL, VALID_PASSWORD)

    # Step 4 & 5: Assert system response
    assert result, (
        "System did not handle extremely long email input as expected. "
        "Expected truncation, validation error, or graceful failure."
    )
