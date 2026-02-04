# Selenium Test Script for TC_LOGIN_002: Invalid Login Scenario
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope='function')
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_with_invalid_credentials(driver):
    """
    TC_LOGIN_002: Test invalid login attempt
    Steps:
        1. Navigate to login page
        2. Enter invalid email
        3. Enter valid password
        4. Click login
        5. Assert error message and no dashboard redirect
    """
    login_page = LoginPage(driver)
    # Step 1: Go to login page
    login_page.go_to_login_page()
    assert login_page.is_login_fields_visible(), "Login fields should be visible on the page."

    # Step 2: Enter invalid email
    email = "invaliduser@example.com"
    assert login_page.enter_email(email), f"Email field value should be '{email}'."

    # Step 3: Enter valid password
    password = "ValidPass123!"
    assert login_page.enter_password(password), "Password field should be masked and accept input."

    # Step 4: Click login and validate negative outcome
    login_page.click_login()
    assert login_page.is_error_message_displayed("Invalid email or password"), "Error message for invalid login should be displayed."
    assert not login_page.is_redirected_to_dashboard(), "User should not be redirected to dashboard on invalid login."

    # Composite method check (optional)
    assert login_page.login_with_invalid_credentials(email, password), "Composite invalid login should return True when error is shown and dashboard is not reached."
