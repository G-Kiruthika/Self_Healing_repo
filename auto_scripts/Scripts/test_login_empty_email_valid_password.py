# Selenium Test Script for TC_LOGIN_004: Login with empty email and valid password
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_with_empty_email_and_valid_password(driver):
    """
    Test Case: TC_LOGIN_004
    Title: Attempt login with empty email and valid password
    Steps:
        1. Navigate to the login page
        2. Leave email field empty
        3. Enter valid password
        4. Click on the Login button
        5. Verify validation error 'Email is required' is displayed and login is prevented
    Acceptance Criteria:
        - Validation error for email is displayed
        - User remains on login page
        - Login is not attempted
    """
    login_page = LoginPage(driver)
    password = "ValidPass123!"  # Replace with actual valid password if needed

    # Step 1: Navigate to the login page
    login_page.go_to_login_page()
    assert driver.current_url == login_page.LOGIN_URL, "Login page URL mismatch."
    assert login_page.is_login_fields_visible(), "Login fields are not visible."

    # Step 2: Leave email field empty (explicitly clear)
    login_page.enter_email("")
    email_value = driver.find_element(*login_page.EMAIL_FIELD).get_attribute("value")
    assert email_value == "", "Email field is not empty."

    # Step 3: Enter valid password
    password_masked = login_page.enter_password(password)
    assert password_masked, "Password field is not masked or not entered."
    password_value = driver.find_element(*login_page.PASSWORD_FIELD).get_attribute("value")
    assert password_value == password, "Password value mismatch."

    # Step 4: Click Login button
    login_page.click_login()

    # Step 5: Verify validation error and login is prevented
    # This uses the PageClass helper for TC_LOGIN_004
    result = login_page.login_with_empty_email_and_valid_password(password)
    assert result, "Validation error for empty email not displayed or login not prevented."
    assert driver.current_url == login_page.LOGIN_URL, "User did not remain on login page after invalid login attempt."
