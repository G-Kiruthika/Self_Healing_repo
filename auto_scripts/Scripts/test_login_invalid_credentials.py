# Selenium Test Script for TC_LOGIN_003: Invalid Credentials
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_with_invalid_credentials(driver):
    """
    Test Case ID: TC_LOGIN_003
    Description: Attempt login with invalid username and valid password. Expect error message and remain on login page.
    Steps:
    1. Navigate to the login page
    2. Enter invalid username
    3. Enter valid password
    4. Click Login button
    5. Verify error message is displayed and user remains on login page
    Acceptance Criteria: Error message 'Invalid username or password' is displayed, user is not authenticated.
    Traceability: Maps to LoginPage.login_with_invalid_credentials()
    """
    login_page = LoginPage(driver)
    invalid_email = "invaliduser@example.com"
    valid_password = "Test@1234"

    # Step 1: Navigate to the login page
    login_page.go_to_login_page()
    assert driver.current_url.startswith(LoginPage.LOGIN_URL), "Login page did not open."

    # Step 2: Enter invalid username
    assert login_page.enter_email(invalid_email), "Invalid username was not entered correctly!"

    # Step 3: Enter valid password
    assert login_page.enter_password(valid_password), "Password was not entered/masked correctly!"

    # Step 4: Click Login button
    login_page.click_login()

    # Step 5: Verify error message is displayed and user remains on login page
    import time
    time.sleep(1)  # Give time for error message to appear
    error_message = login_page.get_error_message()
    assert error_message is not None, "No error message displayed after invalid login!"
    assert "invalid username or password" in error_message.lower(), f"Expected error message not found: {error_message}"
    assert not login_page.is_redirected_to_dashboard(), "User should not be redirected to dashboard on invalid login!"
    assert driver.current_url.startswith(LoginPage.LOGIN_URL), "User did not remain on login page after invalid login!"
