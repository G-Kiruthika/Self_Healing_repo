# Test Script for LGN-01: Verify successful login with valid credentials
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage
import time

@pytest.fixture(scope='module')
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_valid_credentials(driver):
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
    valid_email = 'testuser@example.com'  # Replace with actual valid email
    valid_password = 'TestPassword123!'   # Replace with actual valid password
    login_page.enter_credentials(valid_email, valid_password)
    # Optionally, assert that fields accept input (basic check)
    email_value = driver.find_element(*LoginPage.EMAIL_FIELD).get_attribute('value')
    password_value = driver.find_element(*LoginPage.PASSWORD_FIELD).get_attribute('value')
    assert email_value == valid_email, f"Email field did not accept input. Expected: {valid_email}, Got: {email_value}"
    assert password_value == valid_password, f"Password field did not accept input. Expected: {valid_password}, Got: {password_value}"
    # Step 3: Click Login button
    login_page.click_login()
    # Step 4: Assert redirected to Dashboard
    # Wait for redirection (explicit wait recommended in real scenarios)
    time.sleep(2)
    assert login_page.is_redirected_to_dashboard(), "Login failed or dashboard not visible after login."
