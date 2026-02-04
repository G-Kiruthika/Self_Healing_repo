# Selenium test script for TC_LOGIN_017: Account Lockout after multiple failed attempts
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage
import time

# Test Data for TC_LOGIN_017
test_email = "testuser@example.com"
wrong_passwords = ["WrongPass1", "WrongPass2", "WrongPass3", "WrongPass4", "WrongPass5"]
correct_password = "ValidPass123!"

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_account_lockout(driver):
    """
    TC_LOGIN_017: Test account lockout after multiple failed login attempts
    Steps:
    1. Navigate to the login page
    2. Enter valid email address
    3. Enter incorrect password and attempt login (Attempt 1)
    4. Repeat login with incorrect password (Attempts 2-4)
    5. Attempt login with incorrect password (Attempt 5)
    6. Attempt login with correct password (should remain locked)
    """
    login_page = LoginPage(driver)
    # Step 1: Go to login page
    login_page.go_to_login_page()
    assert login_page.is_login_fields_visible(), "Login fields are not visible!"
    # Step 2: Enter valid email
    assert login_page.enter_email(test_email), "Email was not entered correctly!"
    # Step 3-5: Enter wrong passwords 5 times
    locked = False
    for idx, wrong_pwd in enumerate(wrong_passwords):
        assert login_page.enter_password(wrong_pwd), f"Password was not entered correctly for attempt {idx+1}!"
        login_page.click_login()
        time.sleep(1)  # Wait for error message to appear
        error_message = login_page.get_error_message()
        assert error_message is not None and error_message != '', f"No error message for failed attempt {idx+1}!"
        if idx == 4:  # After 5th failed attempt
            locked = login_page.is_account_locked()
            assert locked, "Account was not locked after 5 failed attempts!"
            assert error_message == "Account locked due to multiple failed attempts", "Lockout error message not displayed!"
    # Step 6: Attempt login with correct password (should remain locked)
    assert login_page.enter_password(correct_password), "Password was not entered correctly for post-lockout attempt!"
    login_page.click_login()
    time.sleep(1)
    error_message = login_page.get_error_message()
    assert locked, "Account should remain locked after correct password attempt!"
    assert error_message == "Account locked due to multiple failed attempts", "Account remains locked but correct message not displayed!"
