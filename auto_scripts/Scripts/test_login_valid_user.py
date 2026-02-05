# Selenium Test Script for TC-LOGIN-001: Valid User Login
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage
import time

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_valid_user(driver):
    """
    Test Case TC-LOGIN-001: Valid Login
    Steps:
    1. Navigate to the login page
    2. Enter valid email
    3. Enter valid password
    4. Click Login
    5. Verify user session is established
    """
    # Test Data
    login_url = "https://app.example.com/login"  # URL from LoginPage class
    valid_email = "testuser@example.com"
    valid_password = "ValidPass123!"

    login_page = LoginPage(driver)

    # Step 1: Navigate to login page
    assert login_page.navigate_to_login(), "Login page did not load correctly (Step 1)"

    # Step 2: Enter valid registered email
    assert login_page.enter_email(valid_email), f"Email '{valid_email}' was not accepted (Step 2)"

    # Step 3: Enter correct password
    assert login_page.enter_password(valid_password), "Password was not accepted or not masked (Step 3)"

    # Step 4: Click on the Login button
    assert login_page.click_login(), "User was not authenticated or dashboard not displayed (Step 4)"

    # Step 5: Verify user session is created
    assert login_page.verify_user_session(), "User session was not established or profile icon not visible (Step 5)"
