# Test Script for LGN-01: Verify successful login with valid credentials
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto-scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope='function')
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_login_valid_credentials(driver):
    """
    TestCase ID: LGN-01
    Description: Verify successful login with valid credentials
    Steps:
      1. Navigate to login page
      2. Enter valid email and password
      3. Click Login button
      4. Verify dashboard is displayed
    """
    # Arrange
    login_page = LoginPage(driver)
    valid_email = "testuser@example.com"  # Replace with a valid test account
    valid_password = "TestPassword123"    # Replace with a valid test password

    # Act & Assert
    # Step 1: Navigate to login page
    login_page.go_to()
    assert driver.current_url.startswith("https://example-ecommerce.com/login"), "Not on Login Page URL"
    # Step 2: Enter valid email and password
    login_page.enter_email(valid_email)
    login_page.enter_password(valid_password)
    email_field = driver.find_element(*LoginPage.EMAIL_INPUT)
    password_field = driver.find_element(*LoginPage.PASSWORD_INPUT)
    assert email_field.get_attribute('value') == valid_email, "Email input failed"
    assert password_field.get_attribute('value') == valid_password, "Password input failed"
    # Step 3: Click Login button
    login_page.click_login()
    # Step 4: Verify dashboard is displayed
    assert login_page.is_dashboard_displayed(), "Dashboard was not displayed after login"
