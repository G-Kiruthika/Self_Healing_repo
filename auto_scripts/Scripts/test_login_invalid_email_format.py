# Test Script for TC_LOGIN_020: Invalid Email Format Validation
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage
import time

@pytest.fixture(scope='function')
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1400, 1000)
    yield driver
    driver.quit()

@pytest.mark.login
@pytest.mark.negative
@pytest.mark.tc_login_020
class TestLoginInvalidEmailFormat:
    def test_login_with_invalid_email_format(self, driver):
        """
        TC_LOGIN_020: Attempt login with invalid email format (missing '@' symbol) and valid password.
        Steps:
        1. Navigate to the login page
        2. Enter invalid email format (missing '@' symbol)
        3. Enter valid password
        4. Click Login button
        5. Verify validation error displayed: 'Please enter a valid email address'
        6. Verify login is prevented and user remains on login page
        """
        login_page = LoginPage(driver)
        invalid_email = "testuserexample.com"  # missing '@'
        valid_password = "ValidPass123!"

        # Step 1: Navigate to login page
        login_page.go_to_login_page()
        assert driver.current_url == login_page.LOGIN_URL, "Login page URL mismatch!"
        assert login_page.is_login_fields_visible(), "Login fields are not visible!"

        # Step 2: Enter invalid email format
        assert login_page.enter_email(invalid_email), "Invalid email format was not entered correctly!"
        email_field_value = driver.find_element(*login_page.EMAIL_FIELD).get_attribute("value")
        assert email_field_value == invalid_email, f"Email field value mismatch: {email_field_value}"

        # Step 3: Enter valid password
        assert login_page.enter_password(valid_password), "Password was not entered/masked correctly!"
        password_field_type = driver.find_element(*login_page.PASSWORD_FIELD).get_attribute("type")
        assert password_field_type == "password", f"Password field type mismatch: {password_field_type}"

        # Step 4: Click Login button
        login_page.click_login()
        time.sleep(1)

        # Step 5: Verify validation error displayed: 'Please enter a valid email address'
        try:
            validation_error = driver.find_element(*login_page.VALIDATION_ERROR)
            assert validation_error.is_displayed(), "Validation error not displayed!"
            assert "please enter a valid email address" in validation_error.text.lower(), f"Unexpected validation error: {validation_error.text}"
        except Exception as e:
            pytest.fail(f"Validation error element not found or not displayed: {e}")

        # Step 6: Verify login is prevented and user remains on login page
        assert driver.current_url == login_page.LOGIN_URL, "User is not on login page after invalid email format!"
