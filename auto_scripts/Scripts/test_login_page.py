# Selenium Pytest Automation Script for LoginPage
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from auto_scripts.Pages.LoginPage import LoginPage
import string
import random
import time

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

# --- TC_LOGIN_001: Valid Login ---
def test_login_successful(driver):
    page = LoginPage(driver)
    email = "testuser@example.com"
    password = "ValidPass123!"
    assert page.login_successful(email, password)

# --- TC_LOGIN_002: Invalid Email, Valid Password ---
def test_login_with_invalid_email_valid_password(driver):
    page = LoginPage(driver)
    invalid_email = "invalid@example"
    valid_password = "ValidPass123!"
    assert page.login_with_invalid_email_valid_password(invalid_email, valid_password)

# --- TC_LOGIN_003: Valid Email, Invalid Password ---
def test_login_with_valid_email_invalid_password(driver):
    page = LoginPage(driver)
    email = "testuser@example.com"
    invalid_password = "WrongPass!"
    assert page.login_with_valid_email_invalid_password(email, invalid_password)

# --- TC_LOGIN_004: Empty Email, Valid Password ---
def test_login_with_empty_email_and_valid_password(driver):
    page = LoginPage(driver)
    password = "ValidPass123!"
    assert page.login_with_empty_email_and_valid_password(password)

# --- TC_LOGIN_005: Valid Email, Empty Password ---
def test_login_with_valid_email_and_empty_password(driver):
    page = LoginPage(driver)
    email = "testuser@example.com"
    assert page.login_with_valid_email_and_empty_password(email)

# --- TC_LOGIN_006: Empty Email and Password ---
def test_login_with_empty_email_and_empty_password(driver):
    page = LoginPage(driver)
    assert page.login_with_empty_email_and_empty_password()

# --- TC_LOGIN_007: Empty Fields Validation ---
def test_empty_fields_validation(driver):
    page = LoginPage(driver)
    assert page.empty_fields_validation()

# --- TC_LOGIN_011: 254-char Email ---
def test_login_with_254_char_email(driver):
    page = LoginPage(driver)
    # Generate a 254-char email
    local = "a" + "1"*62
    domain1 = "b" + "1"*62
    domain2 = "c" + "1"*62
    domain3 = "d" + "1"*61
    email = f"{local}@{domain1}.{domain2}.{domain3}.com"
    assert len(email) == 254
    password = "ValidPass123!"
    assert page.login_with_254_char_email(email, password)

# --- TC_LOGIN_012: 128-char Password ---
def test_login_with_128_char_password(driver):
    page = LoginPage(driver)
    email = "testuser@example.com"
    # 128-char password
    password = (
        "Aa1!Bb2@Cc3#Dd4$Ee5%Ff6^Gg7&Hh8*Ii9(Jj0)Kk1!Ll2@Mm3#Nn4$Oo5%Pp6^Qq7&Rr8*Ss9(Tt0)Uu1!Vv2@Ww3#Xx4$Yy5%Zz6^Aa7&Bb8*Cc9(Dd0)Ee1!Ff2@Gg3#Hh4$"
    )
    assert len(password) == 128
    assert page.login_with_128_char_password(email, password)

# --- TC_LOGIN_012: Email Exceeding Max Length ---
def test_login_with_email_exceeding_max_length(driver):
    page = LoginPage(driver)
    # 320-char email (RFC max, but UI may limit to 254)
    local = "a" + "1"*62
    domain1 = "b" + "1"*62
    domain2 = "c" + "1"*62
    domain3 = "d" + "1"*61
    email_254 = f"{local}@{domain1}.{domain2}.{domain3}.com"
    # Add extra chars to exceed max length
    long_email = email_254 + "extra" * 10
    password = "ValidPass123!"
    assert len(long_email) > 254
    assert page.login_with_email_exceeding_max_length(long_email, password)

# --- TC_LOGIN_013: SQL Injection Attempt ---
def test_login_with_sql_injection(driver):
    page = LoginPage(driver)
    sql_email = "admin'--"
    password = "anything"
    assert page.login_with_sql_injection(sql_email, password)
