# Selenium Test Script for TC_LOGIN_001 - Login Workflow
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage
import time

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

def test_TC_LOGIN_001_successful_login(driver):
    """
    Test Case: TC_LOGIN_001 - End-to-end login workflow for valid credentials.
    Steps:
    1. Navigate to the login page
    2. Enter valid username
    3. Enter valid password
    4. Click Login
    5. Verify user session is created and user is redirected to dashboard
    """
    # Test Data
    email = 'testuser@example.com'
    password = 'Test@1234'

    login_page = LoginPage(driver)

    # Step 1: Navigate to the login page
    login_page.go_to_login_page()
    assert login_page.is_login_fields_visible(), "Login page is not displayed with username and password fields"

    # Step 2: Enter valid username
    assert login_page.enter_email(email), f"Username '{email}' was not entered successfully in the field"

    # Step 3: Enter valid password
    assert login_page.enter_password(password), "Password is not masked or not entered successfully"

    # Step 4: Click Login
    login_page.click_login()
    time.sleep(2)  # Wait for possible redirect
    assert login_page.is_redirected_to_dashboard(), "User is not authenticated or not redirected to dashboard/home page"

    # Step 5: Verify user session is created
    assert login_page.is_session_token_created(), "User session is not active or user details are not displayed"

    # Optional: Call the dedicated workflow method for traceability
    assert login_page.login_and_verify(email, password), "End-to-end login workflow failed"
