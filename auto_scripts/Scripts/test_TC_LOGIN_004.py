# Selenium Test Script for TC_LOGIN_004 - Login with Empty Password
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope='module')
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_TC_LOGIN_004_empty_password(driver):
    """
    Test Case ID: TC_LOGIN_004
    Description: Verify that login is prevented when password field is empty.
    Steps:
        1. Navigate to the login page
        2. Enter valid registered email
        3. Leave password field empty
        4. Click on the Login button
        5. Verify login is prevented and validation error is shown
    Acceptance Criteria:
        - Password field remains empty
        - Validation error displayed: 'Password is required'
        - User remains on login page
    """
    login_page = LoginPage(driver)

    # Step 1: Navigate to the login page
    assert login_page.navigate_to_login(), "Login page is not displayed."

    # Step 2: Enter valid registered email
    valid_email = "testuser@example.com"
    assert login_page.enter_email(valid_email), f"Email '{valid_email}' not accepted in email field."

    # Step 3: Leave password field empty
    assert login_page.leave_password_field_empty(), "Password field is not empty after clearing."

    # Step 4: Click on the Login button
    assert login_page.click_login_button_for_empty_password(), "Validation error 'Password is required' was not displayed."

    # Step 5: Verify login is prevented and user remains on login page
    assert login_page.verify_login_prevented_for_empty_password(), "User was able to proceed with login or did not remain on login page."
