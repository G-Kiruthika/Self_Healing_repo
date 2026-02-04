# Selenium Test Script for TC_LOGIN_011: Login with maximum valid email length
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import sys
import os

# Ensure the Pages directory is in sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../Pages')))
from LoginPage import LoginPage

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

def generate_max_length_email():
    # Generates a 254-character valid email
    # local: 64 chars, domain: 185 chars, TLD: 5 chars (total 254)
    local = 'a' * 64
    domain = 'b' * 63 + '.' + 'c' * 63 + '.' + 'd' * 63
    tld = '.com'
    email = f"{local}@{domain}{tld}"
    assert len(email) == 254, f"Email length is {len(email)}, expected 254"
    return email

def get_valid_password():
    # Replace with actual valid password as per environment
    return "ValidPass123!"

def test_login_with_max_length_email(driver):
    """
    TC_LOGIN_011: Login with maximum valid email length (254 characters) and valid password.
    Steps:
        1. Navigate to the login page
        2. Enter email address with 254 characters
        3. Enter valid password
        4. Click on the Login button
        5. Verify system processes login appropriately (success if registered, error if not)
    Acceptance Criteria: SCRUM-91
    """
    login_page = LoginPage(driver)
    email = generate_max_length_email()
    password = get_valid_password()

    # Step 1: Navigate to login page
    login_page.go_to_login_page()
    assert driver.current_url.startswith("https://app.example.com/login"), "Login page URL mismatch!"
    assert login_page.is_login_fields_visible(), "Login fields are not visible!"

    # Step 2: Enter 254-char email
    assert login_page.enter_email(email), "Email was not entered correctly!"
    actual_email_value = driver.find_element(By.ID, "login-email").get_attribute("value")
    assert actual_email_value == email, f"Email field value mismatch! Expected: {email}, Got: {actual_email_value}"

    # Step 3: Enter valid password
    assert login_page.enter_password(password), "Password was not entered/masked correctly!"
    password_type = driver.find_element(By.ID, "login-password").get_attribute("type")
    assert password_type == "password", "Password field is not masked!"

    # Step 4: Click Login
    login_page.click_login()
    time.sleep(2)  # Wait for system response

    # Step 5: Check outcome (success or error)
    if login_page.is_redirected_to_dashboard():
        assert login_page.is_session_token_created(), "User session was not created after login!"
        print("[TC_LOGIN_011] Login successful with max length email.")
    else:
        error_message = login_page.get_error_message()
        assert error_message is not None, "No error message displayed for failed login!"
        print(f"[TC_LOGIN_011] Login failed as expected. Error message: {error_message}")
