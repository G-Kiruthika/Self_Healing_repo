'''
Selenium Automation Test Script for TC-LOGIN-012: SQL Injection Negative Test

- Validates that SQL injection in the login email field does not grant unauthorized access.
- Uses LoginPage Page Object from auto_scripts.Pages.LoginPage
- Test Data: Email: admin' OR '1'='1, Password: password123
- Acceptance Criteria: TS-010
'''

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    try:
        driver = webdriver.Chrome(options=options)
        yield driver
    finally:
        driver.quit()


def test_tc_login_012_sql_injection_login(driver):
    """
    Test Case TC-LOGIN-012:
    1. Navigate to the login page
    2. Enter SQL injection payload in email field
    3. Enter any password
    4. Click on the Login button
    5. Verify no unauthorized access is granted
    """
    login_page = LoginPage(driver)
    sql_injection_email = "admin' OR '1'='1"
    test_password = "password123"

    # Run the negative test and assert it passes
    assert login_page.tc_login_012_sql_injection_login(sql_injection_email, test_password) is True
