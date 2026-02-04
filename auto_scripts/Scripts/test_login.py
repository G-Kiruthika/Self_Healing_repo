# Selenium Test Script for LoginPage
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
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_successful(driver):
    """TC_LOGIN_001: End-to-end login workflow with valid credentials."""
    login_page = LoginPage(driver)
    email = "testuser@example.com"
    password = "ValidPass123!"
    assert login_page.login_successful(email, password)

def test_login_account_lockout(driver):
    """TC_LOGIN_017: Account lockout after multiple failed attempts."""
    login_page = LoginPage(driver)
    email = "testuser@example.com"
    wrong_passwords = ["WrongPass1", "WrongPass2", "WrongPass3", "WrongPass4", "WrongPass5"]
    correct_password = "ValidPass123!"
    assert login_page.login_account_lockout(email, wrong_passwords, correct_password)

def test_login_invalid_email_format(driver):
    """TC_LOGIN_020: Attempt login with invalid email format."""
    login_page = LoginPage(driver)
    invalid_email = "testuserexample.com"  # missing @
    password = "ValidPass123!"
    assert login_page.login_invalid_email_format(invalid_email, password)

def test_login_invalid_credentials(driver):
    """TC_LOGIN_003: Invalid username, valid password."""
    login_page = LoginPage(driver)
    invalid_email = "invaliduser@example.com"
    valid_password = "Test@1234"
    assert login_page.login_invalid_credentials(invalid_email, valid_password)

def test_login_invalid_credentials_valid_username_invalid_password(driver):
    """TC_LOGIN_004: Valid username, invalid password."""
    login_page = LoginPage(driver)
    valid_email = "testuser@example.com"
    invalid_password = "WrongPass@123"
    assert login_page.login_invalid_credentials_valid_username_invalid_password(valid_email, invalid_password)

def test_login_invalid_credentials_both_invalid(driver):
    """TC_LOGIN_005: Both username and password invalid."""
    login_page = LoginPage(driver)
    invalid_email = "wronguser@example.com"
    invalid_password = "WrongPass@999"
    assert login_page.login_invalid_credentials_both_invalid(invalid_email, invalid_password)
