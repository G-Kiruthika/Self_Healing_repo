# test_login_invalid_credentials.py
"""
Test Case: TC_LOGIN_002
Description: Verify that an error message is displayed when attempting to login with an invalid email and valid password.
Acceptance Criteria: SCRUM-91
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_with_invalid_email(driver):
    login_page = LoginPage(driver)

    # Step 1: Navigate to the login page
    login_page.go_to_login_page()
    assert login_page.is_login_fields_visible(), "Login fields are not visible on the login page."

    # Step 2 & 3: Enter invalid email and valid password
    invalid_email = "invaliduser@example.com"
    valid_password = "ValidPass123!"
    login_page.enter_credentials(invalid_email, valid_password)
    email_field_value = driver.find_element(*LoginPage.EMAIL_FIELD).get_attribute("value")
    password_field_value = driver.find_element(*LoginPage.PASSWORD_FIELD).get_attribute("value")
    assert email_field_value == invalid_email, f"Expected email field to be '{invalid_email}', but got '{email_field_value}'"
    assert password_field_value == valid_password, "Password was not entered correctly."

    # Step 4: Click Login and validate error message
    login_page.click_login()
    assert login_page.is_error_message_displayed("Invalid email or password"), (
        "Expected error message 'Invalid email or password' was not displayed after invalid login."
    )
    # Confirm user remains on login page (dashboard not visible)
    assert not login_page.is_redirected_to_dashboard(), "User should not be redirected to dashboard on invalid login."
