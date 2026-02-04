# Selenium Automation Test Script for TC_LOGIN_020 (Invalid Email Format)
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage
import time

@pytest.mark.usefixtures('driver')
def test_TC_LOGIN_020_invalid_email_format():
    """
    TC_LOGIN_020: Validate login fails with invalid email format (missing @ symbol)
    Steps:
    1. Navigate to the login page
    2. Enter email in invalid format (missing @ symbol)
    3. Enter valid password
    4. Click on the Login button
    5. Validation error 'Please enter a valid email address' is displayed
    """
    # Test Data
    email = "testuserexample.com"  # Invalid email (missing @)
    password = "ValidPass123!"      # Valid password

    # Setup WebDriver
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)

    try:
        login_page = LoginPage(driver)
        login_page.go_to_login_page()
        assert login_page.is_login_fields_visible(), "Login fields are not visible!"
        assert login_page.enter_email(email), "Email was not entered correctly!"
        assert login_page.enter_password(password), "Password was not entered/masked correctly!"
        login_page.click_login()
        time.sleep(1)
        # Check for validation error
        validation_error_elem = None
        try:
            validation_error_elem = driver.find_element(*LoginPage.VALIDATION_ERROR)
            assert validation_error_elem.is_displayed(), "Validation error element not displayed!"
            error_text = validation_error_elem.text.strip()
            assert "valid email address" in error_text.lower(), f"Unexpected error message: {error_text}"
        except Exception:
            assert False, "Validation error element not found!"
    finally:
        driver.quit()
