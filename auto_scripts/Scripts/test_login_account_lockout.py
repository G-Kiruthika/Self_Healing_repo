# Selenium Python Test Script for TC_LOGIN_017: Account Lockout after Failed Attempts
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage
import time

@pytest.fixture(scope='module')
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_account_lockout(driver):
    """
    TC_LOGIN_017: Test Case for account lockout after multiple failed login attempts
    Steps:
      1. Navigate to the login page
      2. Enter valid email address
      3. Enter incorrect password and attempt login (Attempt 1)
      4. Repeat login with incorrect password (Attempts 2-4)
      5. Attempt login with incorrect password (Attempt 5)
      6. Attempt login with correct password (account should remain locked)
    Expected:
      - Each failed attempt displays error message
      - On 5th failed attempt, account is locked and lockout message displayed
      - Further login with correct password is prevented, lockout message persists
    """
    login_page = LoginPage(driver)

    # Test Data
    email = "testuser@example.com"
    wrong_passwords = ["WrongPass1", "WrongPass2", "WrongPass3", "WrongPass4", "WrongPass5"]
    correct_password = "ValidPass123!"

    # Step 1: Navigate to login page
    login_page.go_to_login_page()
    assert login_page.is_login_fields_visible(), "Login fields are not visible!"
    assert driver.current_url == login_page.LOGIN_URL, "Not on login page!"

    # Step 2: Enter valid email
    assert login_page.enter_email(email), "Email was not entered correctly!"

    # Steps 3-5: Attempt login with wrong passwords
    for idx, wrong_password in enumerate(wrong_passwords, 1):
        assert login_page.enter_password(wrong_password), f"Wrong password was not entered correctly for attempt {idx}!"
        login_page.click_login()
        time.sleep(1)
        error_message = login_page.get_error_message()
        assert error_message is not None, f"No error message displayed for attempt {idx}!"
        if idx < 5:
            assert ("invalid" in error_message.lower() or "error" in error_message.lower()), f"Unexpected error message: {error_message}"
            assert driver.current_url == login_page.LOGIN_URL, f"User is not on login page after failed attempt {idx}!"
        else:
            assert ("account locked" in error_message.lower()), f"Account lockout message not displayed: {error_message}"
            assert driver.current_url == login_page.LOGIN_URL, "User is not on login page after account lockout!"

    # Step 6: Attempt login with correct password (should remain locked)
    assert login_page.enter_password(correct_password), "Correct password was not entered correctly after lockout!"
    login_page.click_login()
    time.sleep(1)
    error_message = login_page.get_error_message()
    assert error_message is not None, "No error message displayed after lockout with correct password!"
    assert "account locked" in error_message.lower(), f"Account lockout message not displayed after lockout: {error_message}"
    assert driver.current_url == login_page.LOGIN_URL, "User is not on login page after lockout with correct password!"
