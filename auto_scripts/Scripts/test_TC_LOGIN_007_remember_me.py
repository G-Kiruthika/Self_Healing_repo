# Selenium Test Script for TC_LOGIN_007: Remember Me Functionality
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage
import time
import os
import pickle

LOGIN_URL = "https://app.example.com/login"
EMAIL = "testuser@example.com"
PASSWORD = "ValidPass123!"
COOKIES_FILE = "remember_me_cookies.pkl"

@pytest.fixture(scope="function")
def driver():
    # Set up Chrome options for headless or visible execution
    options = Options()
    options.add_argument("--window-size=1920,1080")
    # Uncomment below to run headless
    # options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


def save_cookies(driver, file_path):
    with open(file_path, 'wb') as file:
        pickle.dump(driver.get_cookies(), file)

def load_cookies(driver, file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Cookies file not found: {file_path}")
    with open(file_path, 'rb') as file:
        cookies = pickle.load(file)
    driver.get(LOGIN_URL)  # Must be on domain to set cookies
    for cookie in cookies:
        # Remove 'sameSite' if present to avoid errors
        cookie.pop('sameSite', None)
        driver.add_cookie(cookie)


def test_TC_LOGIN_007_remember_me(driver):
    """
    Test Case TC_LOGIN_007: Verify 'Remember Me' keeps user logged in after browser restart.
    Steps:
    1. Navigate to login page
    2. Enter valid email and password
    3. Check 'Remember Me' checkbox
    4. Click Login
    5. Assert user is redirected to dashboard
    6. Save cookies
    7. Close browser and start new session
    8. Load cookies and refresh
    9. Assert user is still logged in and redirected to dashboard
    """
    login_page = LoginPage(driver)

    # Step 1: Go to login page
    login_page.go_to_login_page()
    assert driver.current_url == LOGIN_URL, "Login page URL mismatch."
    assert login_page.is_login_fields_visible(), "Login fields are not visible."

    # Step 2: Enter valid credentials
    assert login_page.enter_email(EMAIL), "Email field did not accept input."
    assert login_page.enter_password(PASSWORD), "Password field did not accept input or is not masked."

    # Step 3: Check 'Remember Me' checkbox
    assert login_page.check_remember_me_checkbox(), "'Remember Me' checkbox was not checked."

    # Step 4: Click Login
    login_page.click_login()
    time.sleep(2)  # Wait for possible redirect

    # Step 5: Assert user is redirected to dashboard
    assert login_page.is_redirected_to_dashboard(), "User was not redirected to dashboard after login."
    assert login_page.is_session_token_created(), "Session token was not created after login."

    # Step 6: Save cookies for session persistence
    save_cookies(driver, COOKIES_FILE)

    # Step 7: Simulate browser restart by closing and creating a new driver
    driver.quit()
    time.sleep(1)  # Ensure browser closes
    options = Options()
    options.add_argument("--window-size=1920,1080")
    new_driver = webdriver.Chrome(options=options)
    new_driver.implicitly_wait(10)

    try:
        # Step 8: Load cookies and refresh
        load_cookies(new_driver, COOKIES_FILE)
        new_driver.refresh()
        time.sleep(2)  # Wait for potential redirect

        # Step 9: Assert user is still logged in
        login_page_after_restart = LoginPage(new_driver)
        assert login_page_after_restart.verify_remembered_session(), (
            "User was not remembered after browser restart."
        )
    finally:
        new_driver.quit()
    # Cleanup: Remove cookies file
    if os.path.exists(COOKIES_FILE):
        os.remove(COOKIES_FILE)
