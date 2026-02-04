# Selenium Test Script for LoginPage
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from auto_scripts.Pages.LoginPage import LoginPage
import time

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

@pytest.fixture
def login_page(driver):
    return LoginPage(driver)

# TC_LOGIN_001: End-to-end login workflow with valid credentials.
def test_login_successful(login_page):
    valid_email = "valid.user@example.com"
    valid_password = "ValidPassword123"
    assert login_page.login_successful(valid_email, valid_password) is True

# TC_LOGIN_002: Attempt login with invalid email and valid password.
def test_login_with_invalid_email_valid_password(login_page):
    invalid_email = "invalid.user@example.com"
    valid_password = "ValidPassword123"
    assert login_page.login_with_invalid_email_valid_password(invalid_email, valid_password) is True

# TC_LOGIN_003: Attempt login with valid email and invalid password.
def test_login_with_valid_email_invalid_password(login_page):
    valid_email = "valid.user@example.com"
    invalid_password = "WrongPassword!"
    assert login_page.login_with_valid_email_invalid_password(valid_email, invalid_password) is True

# TC_LOGIN_004: Attempt login with empty email and valid password.
def test_login_with_empty_email_and_valid_password(login_page):
    valid_password = "ValidPassword123"
    assert login_page.login_with_empty_email_and_valid_password(valid_password) is True

# TC_LOGIN_005: Attempt login with valid email and empty password.
def test_login_with_valid_email_and_empty_password(login_page):
    valid_email = "valid.user@example.com"
    assert login_page.login_with_valid_email_and_empty_password(valid_email) is True

# TC_LOGIN_006: Attempt login with both email and password fields empty.
def test_login_with_empty_email_and_empty_password(login_page):
    assert login_page.login_with_empty_email_and_empty_password() is True
