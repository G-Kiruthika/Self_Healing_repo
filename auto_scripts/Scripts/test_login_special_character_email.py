# Selenium Test Script for TC_LOGIN_019
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage
import time

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

def test_login_with_special_character_email(driver):
    """
    Test Case: TC_LOGIN_019
    Title: Login with email containing special characters and valid password
    Acceptance Criteria: SCRUM-91
    Steps:
        1. Navigate to the login page
        2. Enter email with special characters in valid format
        3. Enter valid password
        4. Click on the Login button
        5. Validate email is accepted and password is masked
        6. Check system processes login appropriately (success or error)
    """
    # Test Data
    email = "test.user+tag@example.co.uk"
    password = "ValidPass123!"

    login_page = LoginPage(driver)

    # Step 1: Navigate to the login page
    login_page.go_to_login_page()
    assert login_page.is_login_fields_visible(), "Login fields are not visible!"

    # Step 2: Enter email with special characters
    assert login_page.enter_email(email), f"Email '{email}' was not entered correctly!"

    # Step 3: Enter valid password
    assert login_page.enter_password(password), "Password was not entered/masked correctly!"

    # Step 4: Click on the Login button
    login_page.click_login()

    # Step 5 & 6: Validate outcome (dashboard or error/validation message)
    time.sleep(2)
    if login_page.is_redirected_to_dashboard():
        assert login_page.is_session_token_created(), "User session was not created after login!"
    else:
        # Check for error message or validation error
        try:
            error_displayed = driver.find_element(*login_page.ERROR_MESSAGE).is_displayed()
        except Exception:
            error_displayed = False
        try:
            validation_error = driver.find_element(*login_page.VALIDATION_ERROR).is_displayed()
        except Exception:
            validation_error = False
        assert error_displayed or validation_error, "Neither dashboard nor error/validation message appeared after login!"
