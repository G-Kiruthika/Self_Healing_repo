# Test Script for TC_LOGIN_017: Account Lockout after Multiple Failed Login Attempts
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage
import time

@pytest.fixture(scope='function')
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_TC_LOGIN_017_account_lockout(driver):
    """
    TC_LOGIN_017: Test account lockout after multiple failed attempts, and verify lockout persists after correct password.
    Steps:
    1. Navigate to the login page
    2. Enter valid email and incorrect password, click Login (Attempts 1-5)
    3. Verify error message displayed for each failed attempt
    4. On 5th attempt, verify account lockout error message
    5. Attempt login with correct password
    6. Verify login is prevented, account remains locked
    Acceptance Criteria: AC_009
    """
    login_page = LoginPage(driver)

    email = "testuser@example.com"
    wrong_passwords = ["WrongPass1", "WrongPass2", "WrongPass3", "WrongPass4", "WrongPass5"]
    correct_password = "ValidPass123!"

    # Step 1: Go to login page
    login_page.go_to_login_page()
    assert login_page.is_login_fields_visible(), "Login fields are not visible!"

    # Steps 2-5: Attempt login with wrong passwords, 5 times
    for idx, wrong_password in enumerate(wrong_passwords, 1):
        assert login_page.enter_email(email), f"Email was not entered correctly for attempt {idx}!"
        assert login_page.enter_password(wrong_password), f"Wrong password was not entered correctly for attempt {idx}!"
        login_page.click_login()
        time.sleep(1)  # Wait for error message to appear
        error_message = login_page.get_error_message()
        assert error_message is not None, f"No error message displayed for attempt {idx}!"
        if idx < 5:
            assert ("invalid" in error_message.lower() or "error" in error_message.lower()), f"Unexpected error message on attempt {idx}: {error_message}"
            assert driver.current_url == login_page.LOGIN_URL, f"User is not on login page after failed attempt {idx}!"
        elif idx == 5:
            assert "account locked" in error_message.lower(), f"Expected account lockout message, got: {error_message}"

    # Step 6: Attempt login with correct password after lockout
    assert login_page.enter_email(email), "Email was not entered correctly for locked account!"
    assert login_page.enter_password(correct_password), "Correct password was not entered correctly for locked account!"
    login_page.click_login()
    time.sleep(1)  # Wait for error message to appear
    error_message = login_page.get_error_message()
    assert error_message is not None, "No error message displayed when account is locked!"
    assert "account locked" in error_message.lower(), f"Expected account locked message after correct password, got: {error_message}"
    assert driver.current_url == login_page.LOGIN_URL, "User is not on login page after locked account attempt!"

    print("TC_LOGIN_017: Account lockout scenario verified successfully.")
