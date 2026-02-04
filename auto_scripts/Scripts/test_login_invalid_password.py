# Test script for TC_LOGIN_003: Login with valid email and invalid password
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

def test_login_with_valid_email_and_invalid_password(driver):
    """
    TC_LOGIN_003: Verify that logging in with a valid email and invalid password
    displays an error message and does not redirect to dashboard.
    Acceptance Criteria: SCRUM-91
    """
    login_page = LoginPage(driver)

    # Step 1: Navigate to the login page
    login_page.go_to_login_page()
    assert driver.current_url == LoginPage.LOGIN_URL, "Should be on login page URL"
    assert login_page.is_login_fields_visible(), "Login fields should be visible"

    # Step 2: Enter valid email address
    email = "testuser@example.com"
    assert login_page.enter_email(email), f"Email field should contain '{email}'"

    # Step 3: Enter incorrect password
    wrong_password = "WrongPassword123"
    assert login_page.enter_password(wrong_password), "Password field should be masked and accept input"

    # Step 4: Click Login and assert error message
    login_page.click_login()
    assert login_page.is_error_message_displayed("Invalid email or password"), (
        "Error message 'Invalid email or password' should be displayed"
    )
    assert driver.current_url == LoginPage.LOGIN_URL, "User should remain on the login page after failed login"
    assert not login_page.is_redirected_to_dashboard(), "User should NOT be redirected to dashboard on invalid login"
