# Selenium Test Script for TC_LOGIN_018 - Account Lock Warnings
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

def test_login_account_lock_warnings(driver):
    """
    TC_LOGIN_018: Test repeated login attempts with invalid password and check warning messages for account lockout.
    Steps:
    1. Navigate to the login page [Test Data: URL: https://app.example.com/login]
    2. Enter valid email and incorrect password, then click Login (Attempts 1-2) [Test Data: Email: testuser@example.com, Password: WrongPass1/2]
    3. Attempt login with incorrect password for the 3rd time [Test Data: Email: testuser@example.com, Password: WrongPass3]
    4. Attempt login with incorrect password for the 4th time [Test Data: Email: testuser@example.com, Password: WrongPass4]
    Expected:
      - Standard error message displayed for first two attempts
      - On 3rd attempt: error message with warning 'Invalid credentials. You have 2 more attempts before your account is locked' is displayed
      - On 4th attempt: error message with warning 'Invalid credentials. You have 1 more attempt before your account is locked' is displayed
    """
    login_page = LoginPage(driver)
    email = "testuser@example.com"
    wrong_passwords = ["WrongPass1", "WrongPass2", "WrongPass3", "WrongPass4"]
    # This method contains all necessary assertions
    assert login_page.login_with_account_lock_warnings(email, wrong_passwords) is True
