# Selenium Automation Test Script for TC_LOGIN_013 (SQL Injection Negative Test)
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import AssertionError
import time
import os
import sys

# Add the Pages directory to sys.path for import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Pages')))
from LoginPage import LoginPage

def get_chrome_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    return driver

@pytest.mark.security
@pytest.mark.login
@pytest.mark.parametrize("sql_email, password", [
    ("admin'--", "anything")
])
def test_login_sql_injection_negative(sql_email, password):
    """
    Test Case: TC_LOGIN_013
    Title: Attempt SQL injection in email field and verify application is not vulnerable.
    Acceptance Criteria: SCRUM-91
    Steps:
        1. Navigate to the login page [Test Data: URL: https://app.example.com/login]
        2. Enter SQL injection payload in email field [Test Data: Email: admin'--]
        3. Enter any password [Test Data: Password: anything]
        4. Click on the Login button
        5. Verify login fails with error message, SQL injection is prevented, and no unauthorized access is granted.
    """
    driver = get_chrome_driver()
    try:
        login_page = LoginPage(driver)
        result = login_page.login_with_sql_injection(sql_email, password)
        assert result is True, "SQL injection negative test failed: login_with_sql_injection did not return True."
    finally:
        driver.quit()
