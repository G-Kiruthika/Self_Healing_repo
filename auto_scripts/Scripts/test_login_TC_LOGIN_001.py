# Selenium Automation Test Script for TC_LOGIN_001
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope='function')
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_TC_LOGIN_001_login_successful(driver):
    """
    Test Case ID: TC_LOGIN_001
    Description: End-to-end login workflow with valid credentials.
    Steps:
    1. Navigate to the login page
    2. Enter valid email address
    3. Enter valid password
    4. Click Login button
    5. Verify user session is created and user is redirected to dashboard
    """
    # Test Data
    valid_email = "testuser@example.com"
    valid_password = "ValidPass123!"

    # Instantiate Page Object
    login_page = LoginPage(driver)

    # Step 1: Navigate to login page
    login_page.go_to_login_page()
    assert driver.current_url.startswith(LoginPage.LOGIN_URL), "Did not navigate to login page URL!"

    # Step 2 & 3: Enter credentials
    assert login_page.is_login_fields_visible(), "Login fields not visible!"
    assert login_page.enter_email(valid_email), "Email not entered correctly!"
    assert login_page.enter_password(valid_password), "Password not entered/masked correctly!"

    # Step 4: Click Login
    login_page.click_login()

    # Step 5: Verify dashboard/profile
    assert login_page.is_redirected_to_dashboard(), "User not redirected to dashboard!"
    assert login_page.is_session_token_created(), "Session token not created or user profile not visible!"
