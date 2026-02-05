# Selenium Test Script for TC_SCRUM74_003: Login with Non-Existent Email
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope='module')
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    drv = webdriver.Chrome(options=options)
    drv.implicitly_wait(5)
    yield drv
    drv.quit()

def test_login_with_nonexistent_email(driver):
    """
    TC_SCRUM74_003: Attempt login with a non-existent email and verify error message 'Invalid credentials'
    Steps:
      1. Navigate to the login page
      2. Enter non-existent email
      3. Enter any password
      4. Click on the Login button
      5. Assert 'Invalid credentials' error message is displayed
    """
    # Test Data
    test_email = "nonexistent@example.com"
    test_password = "AnyPass123!"

    login_page = LoginPage(driver)

    # Step 1: Navigate to the login page
    assert login_page.navigate_to_login(), "Login page did not load or email/password fields not visible."

    # Step 2: Enter non-existent email
    assert login_page.enter_nonexistent_email(test_email), f"Failed to enter non-existent email: {test_email}"

    # Step 3: Enter any password
    assert login_page.enter_any_password(test_password), "Password field did not accept input or was not masked."

    # Step 4: Click on the Login button and verify error message
    assert login_page.click_login_and_verify_invalid_credentials(), "Expected error message 'Invalid credentials' was not displayed."
