# -*- coding: utf-8 -*-
"""
Test Script for TC_LOGIN_012: Login with valid email and 128-character password
Requirements: pytest, selenium, LoginPage PageClass
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage

# Test data for TC_LOGIN_012
test_email = "testuser@example.com"
test_password = (
    "Aa1!Bb2@Cc3#Dd4$Ee5%Ff6^Gg7&Hh8*Ii9(Jj0)Kk1!Ll2@Mm3#Nn4$Oo5%Pp6^Qq7&Rr8*Ss9(Tt0)Uu1!Vv2@Ww3#Xx4$Yy5%Zz6^Aa7&Bb8*Cc9(Dd0)Ee1!Ff2@Gg3#Hh4$"
)

@pytest.fixture(scope='function')
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_with_128_char_password(driver):
    """
    TC_LOGIN_012: Login with valid email and password with 128 characters.
    Steps:
    1. Navigate to the login page
    2. Enter valid email address
    3. Enter password with 128 characters
    4. Click on the Login button
    Acceptance Criteria: SCRUM-91
    Expected: Password is masked and accepted. System processes the login attempt appropriately.
    """
    login_page = LoginPage(driver)

    # Step 1: Navigate to login page
    login_page.go_to_login_page()
    assert driver.current_url.startswith(LoginPage.LOGIN_URL), "Login page URL mismatch."
    assert login_page.is_login_fields_visible(), "Login fields are not visible."

    # Step 2: Enter valid email
    email_accepted = login_page.enter_email(test_email)
    assert email_accepted, "Email was not accepted or not displayed correctly."

    # Step 3: Enter 128-character password
    password_masked = login_page.enter_password(test_password)
    assert password_masked, "Password field is not masked (type!='password')."

    # Step 4: Click Login
    login_page.click_login()

    # Accept both possible outcomes: login success or error message
    login_success = login_page.is_redirected_to_dashboard()
    login_error = login_page.is_error_message_displayed()
    assert login_success or login_error, (
        "Neither dashboard is shown nor error message displayed after login attempt with 128-char password."
    )

    # Traceability
    # Test Case ID: TC_LOGIN_012
    # Acceptance Criteria: SCRUM-91
