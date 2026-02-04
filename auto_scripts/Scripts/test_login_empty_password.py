# Selenium Test Script for TC_LOGIN_005: Login with valid email and empty password
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time

from auto_scripts.Pages.LoginPage import LoginPage

# Test Data for TC_LOGIN_005
test_email = "testuser@example.com"
login_url = "https://app.example.com/login"

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

def test_login_with_email_and_empty_password(driver):
    """
    TC_LOGIN_005: Attempt login with valid email and empty password, expect 'Password is required' validation error.
    Steps:
    1. Navigate to the login page
    2. Enter valid email address
    3. Leave password field empty
    4. Click on the Login button
    5. Assert validation error 'Password is required' is displayed below password field and user is not logged in
    """
    login_page = LoginPage(driver)

    # Step 1: Navigate to login page
    login_page.go_to_login_page()
    assert driver.current_url.startswith(login_url), "Should be on the login page."
    assert login_page.is_login_fields_visible(), "Login fields must be visible."

    # Step 2: Enter valid email address
    assert login_page.enter_email(test_email), f"Email '{test_email}' should be entered in the field."

    # Step 3: Leave password field empty
    assert login_page.enter_password("") is True, "Password field should accept empty input."
    password_element = driver.find_element(*LoginPage.PASSWORD_FIELD)
    assert password_element.get_attribute("value") == "", "Password field must remain empty."

    # Step 4: Click on the Login button
    login_page.click_login()

    # Step 5: Assert validation error is displayed and login is prevented
    try:
        validation_error = driver.find_element(*LoginPage.VALIDATION_ERROR)
        assert validation_error.is_displayed(), "Validation error element should be displayed."
        assert "Password is required" in validation_error.text, "Error message should say 'Password is required'."
    except NoSuchElementException:
        pytest.fail("Validation error for empty password not displayed!")

    assert driver.current_url == login_url, "User should remain on the login page after failed login."
    assert not login_page.is_redirected_to_dashboard(), "User must not be redirected to dashboard."
