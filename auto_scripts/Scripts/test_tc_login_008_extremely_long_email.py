'''
Test Script for TC-LOGIN-008: Login with Extremely Long Email Address
Author: Automation Agent
Description:
    - Attempts login with an extremely long email address (255+ characters)
    - Asserts that the system truncates input or shows validation error, and does NOT allow login
    - Uses LoginPage Page Object
'''

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope='module')
def driver():
    # Set up Chrome driver (headless for CI/CD)
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1920, 1080)
    yield driver
    driver.quit()

def test_tc_login_008_extremely_long_email(driver):
    """
    TC-LOGIN-008: Attempt login with an extremely long email address (255+ chars)
    Acceptance:
      - System truncates input or shows validation error
      - Login does not proceed (dashboard/user icon not visible)
    """
    login_page = LoginPage(driver)

    # Test Data
    url = "https://ecommerce.example.com/login"
    long_email = (
        "verylongemailaddress" * 12 + "@example.com"
    )  # >255 chars
    password = "ValidPass123!"

    # Step 1: Navigate to login page
    driver.get(url)

    # Step 2-4: Attempt login with long email
    result = login_page.tc_login_008_extremely_long_email_login(long_email, password)

    # Step 5: Assert system truncates or shows validation error, and login does not succeed
    assert result, (
        f"TC-LOGIN-008 FAILED: Login accepted extremely long email ({len(long_email)} chars) - this is a bug."
    )
