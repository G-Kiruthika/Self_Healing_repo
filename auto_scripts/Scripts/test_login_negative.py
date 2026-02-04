# Selenium Test Script for Negative Login (Invalid Email, Valid Password)
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import sys
import os

# Ensure PageClass import works regardless of test runner location
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Pages')))
from LoginPage import LoginPage

def get_chrome_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(options=options)

@pytest.fixture(scope="function")
def driver():
    driver = get_chrome_driver()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.mark.login
@pytest.mark.negative
class TestLoginNegative:
    def test_login_invalid_email_valid_password(self, driver):
        """
        Test Case TC_LOGIN_002: Negative Login - Invalid Email, Valid Password
        Steps:
        1. Navigate to the login page
        2. Enter invalid email address
        3. Enter valid password
        4. Click on the Login button
        5. Verify error message and user remains on login page
        """
        # Test Data
        login_url = "https://example-ecommerce.com/login"  # Use as per LoginPage.LOGIN_URL
        invalid_email = "invaliduser@example.com"
        valid_password = "ValidPass123!"
        expected_error = "Invalid email or password"

        # Step 1: Navigate to the login page
        login_page = LoginPage(driver)
        login_page.go_to_login_page()
        assert login_page.is_login_fields_visible(), "Login fields are not visible on the login page."

        # Step 2: Enter invalid email address
        login_page.enter_email(invalid_email)
        email_value = driver.find_element(*LoginPage.EMAIL_FIELD).get_attribute('value')
        assert email_value == invalid_email, f"Email field value mismatch. Expected: {invalid_email}, Got: {email_value}"

        # Step 3: Enter valid password (and check masking)
        login_page.enter_password(valid_password)
        password_value = driver.find_element(*LoginPage.PASSWORD_FIELD).get_attribute('value')
        assert password_value == valid_password, "Password field value mismatch."
        assert login_page.is_password_masked(), "Password field is not masked."

        # Step 4: Click on the Login button
        login_page.click_login()
        time.sleep(1)  # Wait for error message to appear (can be replaced with WebDriverWait)

        # Step 5: Verify error message and user remains on login page
        assert login_page.is_error_message_displayed(expected_error), f"Expected error message '{expected_error}' not displayed."
        assert login_page.is_on_login_page(), "User did not remain on login page after invalid login attempt."

        # (Optional) Extra: Ensure not redirected to dashboard
        assert not login_page.is_redirected_to_dashboard(), "User was incorrectly redirected to dashboard with invalid credentials."

# End of test_login_negative.py
