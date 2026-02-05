# Test Script for TC_LOGIN_004: Login with empty password
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from auto_scripts.Pages.LoginPage import LoginPage

# Test Data
test_email = "testuser@example.com"
test_password = ""

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_with_empty_password(driver):
    """
    TC_LOGIN_004: Attempt login with valid email and empty password
    Steps:
    1. Navigate to the login page
    2. Enter valid registered email
    3. Leave password field empty
    4. Click on the Login button
    5. Verify login is prevented, validation error displayed: 'Password is required'
    """
    login_page = LoginPage(driver)

    # Step 1: Navigate to login page
    assert login_page.navigate_to_login(), "Login page did not display correctly."

    # Step 2 & 3: Enter valid email, leave password empty
    assert login_page.enter_valid_email_leave_password_empty(test_email), "Email not accepted or password field not empty."

    # Step 4: Click login and check for 'Password is required' validation error
    assert login_page.click_login_and_verify_password_required(), "Validation error for empty password not displayed."

    # Step 5: Verify login is prevented and user remains on login page
    assert login_page.verify_login_prevented_password_empty(), "User was able to proceed with empty password or did not remain on login page."
