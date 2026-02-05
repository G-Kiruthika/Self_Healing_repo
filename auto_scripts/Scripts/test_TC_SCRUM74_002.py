# Selenium Test Script for TC_SCRUM74_002: Invalid Email Format Login
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_invalid_email_format_login(driver):
    """
    Test Case ID: 192
    Test Case: TC_SCRUM74_002
    Description: Attempt login with invalid email format and valid password. Expect proper validation and error messages.
    Steps:
        1. Navigate to the login page
        2. Enter invalid email format (invalidemail@)
        3. Enter valid password (ValidPass123!)
        4. Click on the Login button
    Acceptance Criteria:
        - Login page is displayed
        - Invalid email format error message is displayed
        - Password is accepted (masked)
        - Login fails with error message 'Invalid email or username'
    """
    login_page = LoginPage(driver)

    # Step 1: Navigate to login page
    assert login_page.navigate_to_login(), "Login page should be displayed."

    # Step 2: Enter invalid email format
    invalid_email = "invalidemail@"
    assert login_page.enter_invalid_email_format(invalid_email), "Invalid email format error message should be displayed."

    # Step 3: Enter valid password
    valid_password = "ValidPass123!"
    assert login_page.enter_valid_password_for_invalid_email(valid_password), "Password should be masked and accepted."

    # Step 4: Click Login and expect error
    assert login_page.click_login_and_expect_invalid_email_error(), "Login should fail with error message 'Invalid email or username'."
