# Selenium Test Script for TC_LOGIN_001: Login Functionality
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage
import time

@pytest.fixture(scope='module')
def driver():
    options = Options()
    options.add_argument('--headless')  # Run in headless mode for CI
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_TC_LOGIN_001_valid_login(driver):
    """
    Test Case ID: TC_LOGIN_001
    Description: Verify that a user can login successfully with valid credentials and is redirected to dashboard.
    Steps:
        1. Navigate to the login page
        2. Enter valid email address in the email field
        3. Enter valid password in the password field
        4. Click on the Login button
        5. Verify user is logged in and dashboard is displayed
    """
    login_page = LoginPage(driver)

    # Step 1: Navigate to the login page
    login_page.go_to_login_page()
    assert driver.current_url.startswith("https://example-ecommerce.com/login"), "Not on Login Page URL."

    # Step 2: Check login fields are visible
    assert login_page.is_login_fields_visible(), "Email or Password field not visible."

    # Step 3: Enter email
    test_email = "testuser@example.com"
    login_page.enter_credentials(test_email, "ValidPass123!")
    email_value = driver.find_element(*login_page.EMAIL_FIELD).get_attribute("value")
    assert email_value == test_email, f"Email field value mismatch: expected {test_email}, got {email_value}"

    # Step 4: Password is entered (masked)
    password_elem = driver.find_element(*login_page.PASSWORD_FIELD)
    password_value = password_elem.get_attribute("value")
    assert password_value == "ValidPass123!", "Password value not set correctly."
    assert password_elem.get_attribute("type") == "password", "Password field is not masked."

    # Step 5: Click Login
    login_page.click_login()
    
    # Wait for dashboard to load
    time.sleep(2)

    # Step 6: Verify dashboard is displayed with user profile
    assert login_page.is_redirected_to_dashboard(), "Dashboard or user profile not displayed after login."
