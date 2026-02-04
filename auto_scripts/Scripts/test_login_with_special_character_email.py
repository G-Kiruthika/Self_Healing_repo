# Selenium test for TC_LOGIN_019: Login with special character email
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import time
import sys
import os

# Adjust import path for PageClass
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Pages')))
from LoginPage import LoginPage

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_with_special_character_email(driver):
    """
    TC_LOGIN_019: Enter email address with special characters in valid format, valid password, and attempt login.
    Steps:
    1. Navigate to the login page [Test Data: URL: https://app.example.com/login] [Acceptance Criteria: SCRUM-91]
    2. Enter email with special characters in valid format [Test Data: Email: test.user+tag@example.co.uk] [Acceptance Criteria: SCRUM-91]
    3. Enter valid password [Test Data: Password: ValidPass123!] [Acceptance Criteria: SCRUM-91]
    4. Click on the Login button [Test Data: N/A] [Acceptance Criteria: SCRUM-91]
    Expected:
    - Email is accepted
    - Password is masked and entered
    - System processes login appropriately based on whether email is registered
    """
    login_page = LoginPage(driver)
    special_email = "test.user+tag@example.co.uk"
    valid_password = "ValidPass123!"

    # Step 1: Navigate to the login page
    login_page.go_to_login_page()
    assert driver.current_url.startswith("https://app.example.com/login"), "Login page URL is not correct!"
    assert login_page.is_login_fields_visible(), "Login fields are not visible!"

    # Step 2: Enter email with special characters
    assert login_page.enter_email(special_email), f"Email '{special_email}' was not entered correctly!"

    # Step 3: Enter valid password
    assert login_page.enter_password(valid_password), "Password was not entered/masked correctly!"

    # Step 4: Click on the Login button
    login_page.click_login()
    time.sleep(1)  # Wait for page response

    # Expected: Either redirected to dashboard or error message shown
    redirected = login_page.is_redirected_to_dashboard()
    error_message = login_page.get_error_message()

    if redirected:
        assert redirected, "User was not redirected to dashboard after login!"
        assert login_page.is_session_token_created(), "User session was not created!"
    else:
        assert error_message is not None, "No error message displayed for unregistered special character email!"
    # Final assertion: one of the two outcomes must occur
    assert redirected or error_message is not None, "Neither dashboard nor error message appeared!"
