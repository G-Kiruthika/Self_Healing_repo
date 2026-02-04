# Test Script for TC_LOGIN_002 - Login with Remember Me checked
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
import time
import os
import sys

# Ensure Pages folder is in the path for import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../Pages')))
from LoginPage import LoginPage

@pytest.fixture(scope='function')
def driver():
    options = Options()
    options.add_argument('--headless')  # Remove if you want to see browser
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_with_remember_me(driver):
    """
    TC_LOGIN_002: Login with Remember Me checked
    Steps:
        1. Navigate to the login page
        2. Enter valid username
        3. Enter valid password
        4. Check the Remember Me checkbox
        5. Click on the Login button
        6. Verify user is authenticated, redirected to dashboard, and session is persisted
    """
    login_page = LoginPage(driver)

    # Test Data
    valid_email = "testuser@example.com"
    valid_password = "Test@1234"

    # Step 1: Navigate to the login page
    login_page.go_to_login_page()
    assert driver.current_url.startswith("https://app.example.com/login"), "Did not reach login page URL!"

    # Step 2: Check login fields are visible
    assert login_page.is_login_fields_visible(), "Login fields are not visible!"

    # Step 3: Enter valid username
    assert login_page.enter_email(valid_email), "Email was not entered correctly!"

    # Step 4: Enter valid password
    assert login_page.enter_password(valid_password), "Password was not entered/masked correctly!"

    # Step 5: Check the Remember Me checkbox
    assert login_page.check_remember_me(), "Remember Me checkbox was not selected!"

    # Step 6: Click Login button
    login_page.click_login()

    # Wait for dashboard to load
    time.sleep(2)

    # Step 7: Verify user is redirected to dashboard
    assert login_page.is_redirected_to_dashboard(), "User was not redirected to dashboard!"

    # Step 8: Verify session is created and user profile is visible
    assert login_page.is_session_token_created(), "User session was not created or profile not visible!"

    # Step 9: Optionally, verify Remember Me session persistence by refreshing
    driver.refresh()
    time.sleep(1)
    assert login_page.is_session_token_created(), "Session did not persist after refresh!"
