# Selenium Test Script for TC_LOGIN_018: Three Failed Login Attempts Warning
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

def test_login_three_failed_attempts_warning(driver):
    """
    TC_LOGIN_018: Attempt login with incorrect password three times, verify warning after third attempt.
    Steps:
    1. Navigate to the login page [Test Data: URL: https://app.example.com/login]
    2. Enter valid email address [Test Data: Email: testuser@example.com]
    3. Attempt login with incorrect password three times [Test Data: Password: WrongPass1, WrongPass2, WrongPass3]
    4. Verify warning message after third attempt: 'Warning: Account will be locked after 2 more failed attempts'
    """
    login_page = LoginPage(driver)
    email = "testuser@example.com"
    wrong_passwords = ["WrongPass1", "WrongPass2", "WrongPass3"]
    # Step 1: Navigate to the login page
    login_page.go_to_login_page()
    assert login_page.is_login_fields_visible(), "Login fields are not visible!"
    # Step 2-4: Perform three failed login attempts and verify warning after third
    for idx, wrong_password in enumerate(wrong_passwords, 1):
        assert login_page.enter_email(email), f"Email was not entered correctly for attempt {idx}!"
        assert login_page.enter_password(wrong_password), f"Wrong password was not entered correctly for attempt {idx}!"
        login_page.click_login()
        time.sleep(1)
        error_message = login_page.get_error_message()
        assert error_message is not None, f"No error message displayed for attempt {idx}!"
        assert driver.current_url == login_page.LOGIN_URL, f"User is not on login page after failed attempt {idx}!"
        if idx == 3:
            assert "Warning: Account will be locked after 2 more failed attempts" in error_message, \
                f"Expected warning message not found on third attempt: {error_message}"
