# Selenium Test Script for LoginPage
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import string
import random
import time
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def random_email(length=260):
    # Generate a random email address exceeding 255 characters
    local_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length-20))
    domain = 'testdomain.com'
    return f"{local_part}@{domain}"

def test_TC_LOGIN_001_successful_login(driver):
    """
    TC_LOGIN_001: End-to-end login workflow with valid credentials.
    """
    login_page = LoginPage(driver)
    # Replace with valid credentials for your environment
    email = "valid.user@example.com"
    password = "ValidPass123!"
    assert login_page.login_successful(email, password) is True

def test_TC_LOGIN_002_invalid_email_valid_password(driver):
    """
    TC_LOGIN_002: Attempt login with invalid email and valid password.
    """
    login_page = LoginPage(driver)
    invalid_email = "invalid.user@example.com"
    valid_password = "ValidPass123!"
    assert login_page.login_with_invalid_email_valid_password(invalid_email, valid_password) is True

def test_TC_LOGIN_003_valid_email_invalid_password(driver):
    """
    TC_LOGIN_003: Attempt login with valid email and invalid password.
    """
    login_page = LoginPage(driver)
    email = "valid.user@example.com"
    invalid_password = "WrongPass!"
    assert login_page.login_with_valid_email_invalid_password(email, invalid_password) is True

def test_TC_LOGIN_004_empty_email_valid_password(driver):
    """
    TC_LOGIN_004: Attempt login with empty email and valid password.
    """
    login_page = LoginPage(driver)
    password = "ValidPass123!"
    assert login_page.login_with_empty_email_and_valid_password(password) is True

def test_TC_LOGIN_005_valid_email_empty_password(driver):
    """
    TC_LOGIN_005: Attempt login with valid email and empty password.
    """
    login_page = LoginPage(driver)
    email = "valid.user@example.com"
    assert login_page.login_with_valid_email_and_empty_password(email) is True

def test_TC_LOGIN_006_empty_email_and_empty_password(driver):
    """
    TC_LOGIN_006: Attempt login with both email and password fields empty.
    """
    login_page = LoginPage(driver)
    assert login_page.login_with_empty_email_and_empty_password() is True

def test_TC_LOGIN_007_empty_fields_validation(driver):
    """
    TC_LOGIN_007: Test Case for empty fields validation.
    """
    login_page = LoginPage(driver)
    assert login_page.empty_fields_validation() is True

def test_TC_LOGIN_012_exceeding_length_email(driver):
    """
    TC_LOGIN_012: Enter email address exceeding maximum allowed length (255+ characters), verify truncation or validation error.
    """
    login_page = LoginPage(driver)
    long_email = random_email(300)
    password = "ValidPass123!"
    assert login_page.login_with_exceeding_length_email(long_email, password) is True
