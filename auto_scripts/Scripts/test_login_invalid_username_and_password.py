# Selenium test script for TC_LOGIN_005: Invalid username and invalid password
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

from auto_scripts.Pages.LoginPage import LoginPage

def get_webdriver():
    # Headless for CI, remove headless for local debug
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    return driver

@pytest.mark.login
@pytest.mark.negative
@pytest.mark.tc_login_005
def test_login_with_invalid_username_and_invalid_password():
    """
    TC_LOGIN_005: Attempt login with invalid username and invalid password; verify error message is displayed: 'Invalid username or password'.
    Steps:
        1. Navigate to the login page
        2. Enter invalid username
        3. Enter invalid password
        4. Click Login button
        5. Verify error message is displayed: 'Invalid username or password'
        6. Verify user remains on login page (not authenticated)
    """
    driver = get_webdriver()
    try:
        login_page = LoginPage(driver)
        invalid_username = "wronguser@example.com"
        invalid_password = "WrongPass@999"

        # Step 1: Navigate to login page
        login_page.go_to_login_page()
        assert login_page.is_login_fields_visible(), "Login fields are not visible!"

        # Step 2: Enter invalid username
        assert login_page.enter_email(invalid_username), "Invalid username was not entered correctly!"

        # Step 3: Enter invalid password
        assert login_page.enter_password(invalid_password), "Invalid password was not entered/masked correctly!"

        # Step 4: Click Login button
        login_page.click_login()
        time.sleep(1)  # Wait for error message

        # Step 5: Verify error message
        error_message = login_page.get_error_message()
        assert error_message is not None, "No error message displayed!"
        assert "invalid username or password" in error_message.lower(), f"Unexpected error message: {error_message}"

        # Step 6: Verify user remains on login page
        assert driver.current_url == login_page.LOGIN_URL, "User is not on login page after failed login!"

    finally:
        driver.quit()
