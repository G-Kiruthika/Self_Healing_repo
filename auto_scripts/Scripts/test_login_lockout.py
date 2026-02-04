# test_login_lockout.py
# Selenium automation script for TC_LOGIN_016: Account Lockout after Failed Login Attempts
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope='function')
def driver():
    options = Options()
    options.add_argument('--headless')  # Remove if you want to see the browser
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_account_lockout_after_failed_logins(driver):
    """
    TC_LOGIN_016: Attempt login with valid email and incorrect password 5 times, then verify account lockout and lockout message.
    Steps:
        1. Navigate to the login page
        2. Enter valid email and incorrect password, click Login (Attempt 1)
        3. Repeat login with incorrect password (Attempts 2-4)
        4. Attempt login with incorrect password for the 5th time
        5. Attempt login with correct password, expect lockout message
    Acceptance Criteria: SCRUM-91
    """
    login_page = LoginPage(driver)
    email = "testuser@example.com"
    wrong_passwords = [
        "WrongPass1",
        "WrongPass2",
        "WrongPass3",
        "WrongPass4",
        "WrongPass5"
    ]
    correct_password = "ValidPass123!"
    lockout_message = "Account has been locked due to multiple failed login attempts. Please try again after 30 minutes or reset your password"

    # Step 1: Navigate to login page
    login_page.go_to_login_page()
    assert login_page.is_login_fields_visible(), "Login fields are not visible on the login page."
    assert driver.current_url == LoginPage.LOGIN_URL, f"Not on login page: {driver.current_url}"

    # Step 2-4: 5 failed login attempts, expect error message then lockout
    for i in range(4):
        login_page.enter_email(email)
        login_page.enter_password(wrong_passwords[i])
        login_page.click_login()
        time.sleep(1)
        assert login_page.is_error_message_displayed(), f"Error message not displayed after failed login attempt {i+1}."
        assert driver.current_url == LoginPage.LOGIN_URL, "Should remain on login page after failed attempt."

    # 5th failed attempt triggers lockout
    login_page.enter_email(email)
    login_page.enter_password(wrong_passwords[4])
    login_page.click_login()
    time.sleep(1)
    try:
        error_element = driver.find_element(By.CSS_SELECTOR, "div.alert-danger")
        assert error_element.is_displayed(), "Lockout error message not displayed after 5th failed attempt."
        assert lockout_message in error_element.text, f"Expected lockout message not found. Actual: {error_element.text}"
    except NoSuchElementException:
        pytest.fail("Lockout error message element not found after 5th failed login attempt.")
    assert driver.current_url == LoginPage.LOGIN_URL, "Should remain on login page after account lockout."

    # Step 5: Attempt login with correct password (should still be locked)
    login_page.enter_email(email)
    login_page.enter_password(correct_password)
    login_page.click_login()
    time.sleep(1)
    try:
        error_element = driver.find_element(By.CSS_SELECTOR, "div.alert-danger")
        assert error_element.is_displayed(), "Lockout error message not displayed after correct password attempt."
        assert lockout_message in error_element.text, f"Expected lockout message not found after correct password attempt. Actual: {error_element.text}"
    except NoSuchElementException:
        pytest.fail("Lockout error message element not found after correct password attempt.")
    assert driver.current_url == LoginPage.LOGIN_URL, "Should remain on login page after correct password attempt while locked."

    # Optionally, use the PageClass method for further validation
    result = login_page.login_lockout_after_failed_attempts(email, wrong_passwords, correct_password, lockout_message)
    assert result, "login_lockout_after_failed_attempts() did not return True as expected."
