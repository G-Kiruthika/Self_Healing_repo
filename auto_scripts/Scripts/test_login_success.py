# test_login_success.py
# Test script for LGN-01: Verify successful login with valid credentials
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage

# Test data (replace with valid credentials for your environment)
VALID_EMAIL = "testuser@example.com"
VALID_PASSWORD = "secure_password123"

@pytest.fixture(scope='function')
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_login_with_valid_credentials(driver):
    """
    LGN-01: Verify successful login with valid credentials
    Steps:
      1. Navigate to login page
      2. Enter valid email and password
      3. Click Login button
    Expected Results:
      - Login fields are visible
      - Fields accept input
      - Redirected to Dashboard
    """
    login_page = LoginPage(driver)
    # Step 1: Navigate to login page
    login_page.go_to()
    assert driver.current_url.startswith("https://example-ecommerce.com/login"), "Not on login page URL"
    # Assert login fields are visible
    assert driver.find_element(*LoginPage.EMAIL_FIELD).is_displayed(), "Email field not visible"
    assert driver.find_element(*LoginPage.PASSWORD_FIELD).is_displayed(), "Password field not visible"

    # Step 2: Enter valid email and password
    login_page.enter_email(VALID_EMAIL)
    login_page.enter_password(VALID_PASSWORD)
    # Assert fields accept input
    assert driver.find_element(*LoginPage.EMAIL_FIELD).get_attribute('value') == VALID_EMAIL, "Email not entered correctly"
    assert driver.find_element(*LoginPage.PASSWORD_FIELD).get_attribute('value') == VALID_PASSWORD, "Password not entered correctly"

    # Step 3: Click Login button
    login_page.click_login()
    # Assert redirected to Dashboard
    assert login_page.is_dashboard_loaded(), "Dashboard was not loaded after login"
