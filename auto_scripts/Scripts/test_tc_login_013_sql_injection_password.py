'''
Test Script for TC-LOGIN-013: SQL Injection in Password Field
This test validates that SQL injection in the password field is properly sanitized and does not allow unauthorized access. It uses the LoginPage Page Object.
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
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_tc_login_013_sql_injection_password(driver):
    """
    Test Case TC-LOGIN-013: SQL Injection in Password Field
    Steps:
        1. Navigate to the login page
        2. Enter valid email address
        3. Enter SQL injection payload in password field
        4. Click on the Login button
        5. Verify no unauthorized access is granted and error is shown
    Acceptance Criteria:
        - Login fails with error message
        - SQL injection is not successful (dashboard/user icon not present)
        - User is not authenticated, database not compromised
    """
    login_page = LoginPage(driver)
    # Use default test data as per PageClass
    result = login_page.tc_login_013_sql_injection_password(
        email="testuser@example.com",
        injection_password="' OR '1'='1' --"
    )
    assert result, (
        "[TC-LOGIN-013] SQL injection in password field was NOT prevented. "
        "Unauthorized access may have been granted or error message not shown."
    )
