# Selenium Automation Test Script for TC_LOGIN_016 (XSS in Email Field)
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
import time
import os
import sys

# Ensure Pages directory is in sys.path for import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../Pages')))
from LoginPage import LoginPage

@pytest.fixture(scope='function')
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_xss_email_field_tc_login_016(driver):
    """
    TC_LOGIN_016: Verify that XSS payload in email field does not trigger script execution.
    Steps:
    1. Navigate to the login page
    2. Enter XSS script payload in email field
    3. Enter any password
    4. Click on the Login button
    5. Verify no script execution (no alert popup, input sanitized/rejected)
    """
    login_page = LoginPage(driver)
    xss_payload = "<script>alert('XSS')</script>@test.com"
    password = "TestPass123"
    # Step 1: Navigate to login page
    login_page.go_to_login_page()
    assert login_page.is_login_fields_visible(), "Login fields are not visible!"
    # Step 2,3,4,5: Run the XSS test method from PageClass
    result = login_page.test_xss_email_field_tc_login_016(xss_payload, password)
    assert result is True, "TC_LOGIN_016 failed: XSS vulnerability detected or input not properly handled."
