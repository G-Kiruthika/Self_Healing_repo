# Test Script for TC_LOGIN_004: Valid Username, Invalid Password
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage
import time

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_valid_username_invalid_password(driver):
    """
    TC_LOGIN_004: Attempt login with valid username and invalid password, expect error and remain on login page.
    Steps:
        1. Navigate to the login page
        2. Enter valid username
        3. Enter invalid password
        4. Click on the Login button
        5. Verify error message is displayed: 'Invalid username or password' and user remains on login page
    """
    login_page = LoginPage(driver)
    valid_email = "testuser@example.com"
    invalid_password = "WrongPass@123"
    # This method contains all relevant asserts and returns True if successful
    assert login_page.login_valid_username_invalid_password(valid_email, invalid_password)
