# Selenium Pytest Automation Script for TC_LOGIN_012: Login with 128-character password
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage
import string
import random
import time

@pytest.fixture(scope='function')
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def generate_128_char_password():
    # Example: Aa1!Bb2@Cc3#... (repeat pattern to get 128 chars)
    pattern = 'Aa1!Bb2@Cc3#Dd4$Ee5%Ff6^Gg7&Hh8*Ii9(Jj0)Kk1!Ll2@Mm3#Nn4$Oo5%Pp6^Qq7&Rr8*Ss9(Tt0)Uu1!Vv2@Ww3#Xx4$Yy5%Zz6^Aa7&Bb8*Cc9(Dd0)Ee1!Ff2@Gg3#Hh4$'
    assert len(pattern) == 128
    return pattern

@pytest.mark.login
@pytest.mark.positive
@pytest.mark.usefixtures('driver')
def test_login_with_128_char_password(driver):
    """
    TC_LOGIN_012: Enter valid email and 128-character password, verify password is masked and accepted, and system processes login attempt.
    Steps:
    1. Navigate to the login page [Test Data: URL: https://app.example.com/login]
    2. Enter valid email address [Test Data: Email: testuser@example.com]
    3. Enter password with 128 characters [Test Data: Password: <128-char string>]
    4. Click on the Login button
    Acceptance Criteria: Login page is displayed, email is entered, password is masked and accepted, system processes login appropriately
    """
    login_page = LoginPage(driver)
    email = "testuser@example.com"
    password = generate_128_char_password()

    # Step 1: Navigate to the login page
    login_page.go_to_login_page()
    assert driver.current_url.startswith(LoginPage.LOGIN_URL), "Login page URL is not loaded!"
    assert login_page.is_login_fields_visible(), "Login fields are not visible!"

    # Step 2: Enter valid email address
    assert login_page.enter_email(email), "Email was not entered correctly!"
    email_field = driver.find_element(*LoginPage.EMAIL_FIELD)
    assert email_field.get_attribute("value") == email, "Email value mismatch in field!"

    # Step 3: Enter password with 128 characters
    assert len(password) == 128, "Password is not 128 characters!"
    assert login_page.enter_password(password), "Password was not entered/masked correctly!"
    password_field = driver.find_element(*LoginPage.PASSWORD_FIELD)
    assert password_field.get_attribute("type") == "password", "Password field is not masked!"
    assert password_field.get_attribute("value") == password, "Password value mismatch in field!"

    # Step 4: Click on the Login button
    login_page.click_login()
    time.sleep(2)  # Wait for login to process

    # Acceptance Criteria: System processes login appropriately
    redirected = login_page.is_redirected_to_dashboard()
    if redirected:
        assert redirected, "User should be redirected to dashboard for valid credentials!"
        assert login_page.is_session_token_created(), "Session token not created after login!"
    else:
        error_message = login_page.get_error_message()
        assert error_message is not None, "No error message displayed for failed login!"
        # Optionally, check for specific error content
        # assert "invalid email or password" in error_message.lower(), f"Unexpected error message: {error_message}"
        assert driver.current_url == LoginPage.LOGIN_URL, "User is not on login page after failed login!"
