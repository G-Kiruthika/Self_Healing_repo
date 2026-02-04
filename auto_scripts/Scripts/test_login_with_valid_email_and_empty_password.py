# Selenium Test Script for TC_LOGIN_005: Login with valid email and empty password
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage
import time

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

def test_login_with_valid_email_and_empty_password(driver):
    """
    Test Case: TC_LOGIN_005
    Steps:
        1. Navigate to the login page
        2. Enter valid email address
        3. Leave password field empty
        4. Click Login button
        5. Verify validation error 'Password is required' is displayed below password field
        6. Verify login is prevented and user remains on login page
    """
    login_page = LoginPage(driver)
    valid_email = "testuser@example.com"
    # Step 1: Navigate to login page
    login_page.go_to_login_page()
    assert login_page.is_login_fields_visible(), "Login fields are not visible!"
    # Step 2: Enter valid email
    assert login_page.enter_email(valid_email), "Email was not entered correctly!"
    # Step 3: Leave password field empty
    password_field = driver.find_element(*LoginPage.PASSWORD_FIELD)
    password_field.clear()
    assert password_field.get_attribute("value") == "", "Password field is not empty!"
    # Step 4: Click Login button
    login_page.click_login()
    time.sleep(1)  # Wait for validation error
    # Step 5: Verify validation error for password
    from selenium.common.exceptions import NoSuchElementException
    try:
        validation_error = driver.find_element(*LoginPage.VALIDATION_ERROR)
        assert validation_error.is_displayed(), "Validation error not displayed!"
        assert "password is required" in validation_error.text.lower(), f"Unexpected validation error: {validation_error.text}"
    except NoSuchElementException:
        pytest.fail("Validation error element not found!")
    # Step 6: Verify user remains on login page (login not attempted)
    assert driver.current_url == LoginPage.LOGIN_URL, "User did not remain on login page after failed login!"
