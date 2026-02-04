# Test Script for TC_LOGIN_008: Login Without Remember Me
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage
import time

@pytest.fixture(scope='function')
def driver():
    options = Options()
    options.add_argument('--headless')  # Remove if you want to see the browser
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_without_remember_me(driver):
    """
    TC_LOGIN_008: Login with valid credentials, leave 'Remember Me' unchecked, close and restart browser, verify user is logged out.
    Steps:
    1. Navigate to the login page
    2. Enter valid email and password
    3. Ensure 'Remember Me' is unchecked
    4. Click on Login button
    5. Close and restart browser
    6. Navigate to the application
    7. Assert user is redirected to login page (not dashboard)
    """
    EMAIL = "testuser@example.com"
    PASSWORD = "ValidPass123!"
    LOGIN_URL = "https://app.example.com/login"

    # Step 1: Navigate to login page
    login_page = LoginPage(driver)
    login_page.go_to_login_page()
    assert login_page.is_login_fields_visible(), "Login fields are not visible"
    assert login_page.is_forgot_password_link_visible(), "Forgot Password link not visible"
    # Check Remember Me checkbox is present and unchecked
    checkbox = driver.find_element(*LoginPage.REMEMBER_ME_CHECKBOX)
    assert not checkbox.is_selected(), "Remember Me checkbox should be unchecked by default"

    # Step 2: Enter valid email
    assert login_page.enter_email(EMAIL), "Email was not entered correctly"

    # Step 3: Enter valid password
    assert login_page.enter_password(PASSWORD), "Password was not entered or not masked"

    # Step 4: Ensure Remember Me is unchecked
    assert not checkbox.is_selected(), "Remember Me checkbox should remain unchecked"

    # Step 5: Click on Login button
    login_page.click_login()
    # Wait for redirect
    time.sleep(2)
    assert login_page.is_redirected_to_dashboard(), "User was not redirected to dashboard after login"

    # Step 6: Close and restart browser
    cookies = driver.get_cookies()  # Should not be used for restoring session
    driver.quit()
    # Start a new browser session (simulating browser restart)
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    new_driver = webdriver.Chrome(options=options)
    new_driver.implicitly_wait(10)
    try:
        # Step 7: Navigate to the application
        new_login_page = LoginPage(new_driver)
        new_login_page.go_to_login_page()
        time.sleep(2)  # Wait for possible redirect
        # Assert user is redirected to login page (not dashboard)
        assert new_login_page.is_login_fields_visible(), "User is not redirected to login page after browser restart"
        assert not new_login_page.is_redirected_to_dashboard(), "User should not be redirected to dashboard after browser restart"
    finally:
        new_driver.quit()
