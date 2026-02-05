'''
Selenium Automation Test Script for TC-LOGIN-005: Login attempt with empty password field
- Validates strict error handling and page state after login attempt
- Uses LoginPage PageClass from auto_scripts/Pages/LoginPage.py
- Designed for pytest execution
'''

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

@pytest.mark.tc_login_005
def test_login_with_empty_password(driver):
    """
    Test Case: TC-LOGIN-005
    Steps:
    1. Navigate to the login page
    2. Enter valid email address (testuser@example.com)
    3. Leave the password field empty
    4. Click the Login button
    5. Verify validation error is displayed
    6. Verify user remains on login page (no authentication)
    """
    login_page = LoginPage(driver)
    email = "testuser@example.com"
    # Execute the PageClass method for TC-LOGIN-005
    result = login_page.tc_login_005_login_with_empty_password(email)
    assert result is True, "TC-LOGIN-005 scenario failed: validation error or page state incorrect"
