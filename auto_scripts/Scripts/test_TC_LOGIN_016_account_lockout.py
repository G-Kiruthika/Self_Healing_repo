# Selenium Test Script for TC_LOGIN_016: Account Lockout Scenario
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
    # You may need to specify the path to chromedriver
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.mark.account_lockout
class TestAccountLockout:
    def test_account_lockout_after_failed_attempts(self, driver):
        """
        TC_LOGIN_016: Attempt login with incorrect password 5 times to trigger account lockout,
        then attempt with correct password to verify lockout persists.
        Steps:
        1. Navigate to the login page
        2. Enter valid email and incorrect password, click Login (Attempt 1)
        3. Repeat login with incorrect password (Attempts 2-4)
        4. Attempt login with incorrect password for 5th time
        5. Attempt login with correct password (should still be locked)
        Acceptance Criteria: SCRUM-91
        """
        login_page = LoginPage(driver)
        email = "testuser@example.com"
        valid_password = "ValidPass123!"
        wrong_passwords = ["WrongPass1", "WrongPass2", "WrongPass3", "WrongPass4", "WrongPass5"]
        lockout_message = "Account has been locked due to multiple failed login attempts. Please try again after 30 minutes or reset your password"

        # Use the PageObject method for lockout scenario
        result = login_page.login_with_account_lockout(
            email=email,
            valid_password=valid_password,
            wrong_passwords=wrong_passwords,
            lockout_message=lockout_message
        )
        assert result, "Account lockout scenario failed. Lockout message or login block not enforced as expected."

        # Additional traceability: validate error message after lockout attempt
        try:
            error_element = driver.find_element(*login_page.ERROR_MESSAGE)
            assert error_element.is_displayed(), "Error message not displayed after lockout."
            assert lockout_message in error_element.text, f"Expected lockout message not found. Actual: {error_element.text}"
        except Exception as e:
            pytest.fail(f"Error message validation after lockout failed: {e}")

        # Ensure still on login page, not redirected to dashboard
        assert driver.current_url == login_page.LOGIN_URL, "User was redirected off login page after lockout."
        assert not login_page.is_redirected_to_dashboard(), "User should NOT be redirected to dashboard after lockout."
