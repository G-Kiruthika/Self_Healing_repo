# Selenium Pytest Script for TC_LOGIN_004: Login with empty email and valid password
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from auto_scripts.Pages.LoginPage import LoginPage
import time

@pytest.fixture(scope='module')
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
    TC_LOGIN_004: Attempt login with empty email and valid password; verify validation error for email is displayed.
    Steps:
    1. Navigate to the login page
    2. Leave email field empty
    3. Enter valid password
    4. Click Login button
    5. Verify validation error 'Email is required' is displayed below email field
    Acceptance Criteria: AC_003
    """
    login_page = LoginPage(driver)
    valid_password = "ValidPass123!"  # Replace with actual valid password if needed

    # Step 1: Navigate to the login page
    login_page.go_to_login_page()
    assert login_page.is_login_fields_visible(), "Login fields are not visible!"
    
    # Step 2: Leave email field empty
    assert login_page.enter_email("") is True, "Email field is not empty!"
    
    # Step 3: Enter valid password
    assert login_page.enter_password(valid_password), "Password was not entered/masked correctly!"
    
    # Step 4: Click Login button
    login_page.click_login()
    time.sleep(1)  # Wait for validation error

    # Step 5: Verify validation error 'Email is required' is displayed below email field
    try:
        validation_error = driver.find_element(*LoginPage.VALIDATION_ERROR)
        assert validation_error.is_displayed(), "Validation error not displayed!"
        assert "email is required" in validation_error.text.lower(), f"Unexpected validation error: {validation_error.text}"
    except NoSuchElementException:
        pytest.fail("Validation error element not found!")
    
    # Step 6: Verify user remains on login page (login not attempted)
    assert driver.current_url == LoginPage.LOGIN_URL, "User is not on login page after failed login!"
