# Selenium test for TC_LOGIN_003: Invalid Credentials
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

def test_login_invalid_credentials(driver):
    """
    TC_LOGIN_003: Test login with invalid username and valid password.
    Steps:
        1. Navigate to the login page
        2. Enter invalid username
        3. Enter valid password
        4. Click Login button
        5. Verify error message is displayed and user remains on login page
    """
    login_page = LoginPage(driver)
    invalid_email = "invaliduser@example.com"
    valid_password = "Test@1234"
    # Step 1: Navigate to the login page
    login_page.go_to_login_page()
    assert driver.current_url.startswith(LoginPage.LOGIN_URL), "Failed to navigate to login page."
    # Step 2: Enter invalid username
    assert login_page.enter_email(invalid_email), "Invalid username was not entered correctly!"
    # Step 3: Enter valid password
    assert login_page.enter_password(valid_password), "Password was not entered/masked correctly!"
    # Step 4: Click Login button
    login_page.click_login()
    time.sleep(1)  # Wait for error message
    error_message = login_page.get_error_message()
    # Step 5: Verify error message and user remains on login page
    assert error_message is not None, "Error message was not displayed!"
    assert "invalid username or password" in error_message.lower(), f"Unexpected error message: {error_message}"
    assert driver.current_url == LoginPage.LOGIN_URL, "User was redirected away from login page!"
