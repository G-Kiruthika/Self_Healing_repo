# Selenium Test Script for LoginPage
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
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

@pytest.fixture
def login_page(driver):
    return LoginPage(driver)

# TC_LOGIN_001: End-to-end login workflow with valid credentials
def test_login_successful(login_page):
    email = "validuser@example.com"
    password = "ValidPass123!"
    assert login_page.login_successful(email, password)

# TC_LOGIN_017: Account lockout after multiple failed attempts
def test_login_account_lockout(login_page):
    email = "testuser@example.com"
    wrong_passwords = ["WrongPass1", "WrongPass2", "WrongPass3", "WrongPass4", "WrongPass5"]
    correct_password = "ValidPass123!"
    assert login_page.login_account_lockout(email, wrong_passwords, correct_password)

# TC_LOGIN_020: Invalid email format validation
def test_login_invalid_email_format(login_page):
    invalid_email = "testuserexample.com"  # missing '@'
    password = "ValidPass123!"
    assert login_page.login_invalid_email_format(invalid_email, password)

# TC_LOGIN_003: Invalid credentials (invalid username, valid password)
def test_login_invalid_credentials(login_page):
    invalid_email = "invaliduser@example.com"
    valid_password = "Test@1234"
    assert login_page.login_invalid_credentials(invalid_email, valid_password)

# TC_LOGIN_018: Three failed attempts warning
def test_login_three_failed_attempts_warning(login_page):
    email = "testuser@example.com"
    wrong_passwords = ["WrongPass1", "WrongPass2", "WrongPass3"]
    assert login_page.login_three_failed_attempts_warning(email, wrong_passwords)

# TC_LOGIN_004: Valid username, invalid password
def test_login_invalid_credentials_valid_username_invalid_password(login_page):
    valid_email = "testuser@example.com"
    invalid_password = "WrongPass@123"
    assert login_page.login_invalid_credentials_valid_username_invalid_password(valid_email, invalid_password)

# TC_LOGIN_007: Empty fields validation
def test_login_empty_fields_validation(login_page):
    assert login_page.login_empty_fields_validation()
