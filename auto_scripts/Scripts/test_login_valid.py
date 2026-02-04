# test_login_valid.py
# Test Case ID: LGN-01
# Description: Verify successful login with valid credentials

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage
import time

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_success(driver):
    """
    LGN-01: Verify successful login with valid credentials
    Steps:
    1. Navigate to login page
    2. Enter valid email and password
    3. Click Login button
    4. Assert redirected to Dashboard
    """
    login_page = LoginPage(driver)

    # Step 1: Navigate to login page
    login_page.go_to_login_page()
    assert login_page.is_login_fields_visible(), "Login fields are not visible on the login page."

    # Step 2: Enter valid email and password
    valid_email = "testuser@example.com"  # Replace with actual valid test user
    valid_password = "ValidPassword123"   # Replace with actual valid password
    login_page.enter_credentials(valid_email, valid_password)
    # Fields accept input: Selenium will throw if not interactable; no explicit assert needed

    # Step 3: Click Login button
    login_page.click_login()
    # Optional: Wait for navigation
    time.sleep(2)

    # Step 4: Assert redirected to Dashboard
    assert login_page.is_redirected_to_dashboard(), "User is not redirected to Dashboard after login."
