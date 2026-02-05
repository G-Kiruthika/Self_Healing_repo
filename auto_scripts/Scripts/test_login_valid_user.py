# Selenium Test Script for TC-LOGIN-001: Valid User Login
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_tc_login_001_valid_user_login(driver):
    """
    TC-LOGIN-001: Verify that a registered user can log in with valid credentials
    Steps:
    1. Navigate to the e-commerce website login page
    2. Enter valid registered email address in the email field
    3. Enter correct password in the password field
    4. Click on the Login button
    5. Verify user session is established
    """
    login_page = LoginPage(driver)

    # Step 1: Navigate to Login Page
    assert login_page.navigate_to_login(), "Login page is not displayed with email and password fields."

    # Step 2: Enter valid registered email
    valid_email = "testuser@example.com"
    assert login_page.enter_email(valid_email), f"Email '{valid_email}' was not accepted or not displayed in the field."

    # Step 3: Enter correct password
    valid_password = "ValidPass123!"
    assert login_page.enter_password(valid_password), "Password was not masked or not accepted."

    # Step 4: Click Login
    assert login_page.click_login(), "User was not redirected to dashboard/home page after login."

    # Step 5: Verify user session
    assert login_page.verify_user_session(), "User session not established: username not displayed or session cookie missing."
