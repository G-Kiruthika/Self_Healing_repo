# Selenium Test Script for TC_SCRUM74_003 - Login with Non-Existent Email
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import sys
import os

# Ensure Pages directory is importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Pages')))
from LoginPage import LoginPage

@pytest.fixture(scope="module")
def driver():
    # Setup Chrome WebDriver (headless for CI compatibility)
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_with_non_existent_email(driver):
    """
    Test Case ID: TC_SCRUM74_003
    Description: Login attempt with non-existent email should fail with 'Invalid credentials' error.
    """
    login_page = LoginPage(driver)

    # Step 1: Navigate to the login page
    assert login_page.navigate_to_login(), "Login page should be displayed"

    # Step 2: Enter non-existent email
    test_email = "nonexistent@example.com"
    assert login_page.enter_non_existent_email(test_email), f"Email '{test_email}' should be accepted in the field"

    # Step 3: Enter any password
    test_password = "AnyPass123!"
    assert login_page.enter_any_password(test_password), "Password should be masked and accepted"

    # Step 4: Click on the Login button and verify error message
    assert login_page.click_login_and_verify_invalid_credentials(), "Login should fail with 'Invalid credentials' error message"
