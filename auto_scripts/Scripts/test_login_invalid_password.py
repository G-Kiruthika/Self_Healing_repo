# test_login_invalid_password.py
"""
Selenium Automation Test Script for TC_LOGIN_003
Verifies that login with valid email and invalid password fails and user remains on login page.
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage

# Test Data
test_email = "testuser@example.com"
test_wrong_password = "WrongPassword123"
login_url = "https://app.example.com/login"

@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument('--headless')  # Run in headless mode for CI/CD
    options.add_argument('--disable-gpu')
    # You may need to set the path to chromedriver or use webdriver-manager for portability
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

class TestLoginInvalidPassword:
    def test_login_with_valid_email_and_invalid_password(self, driver):
        """
        Test Case TC_LOGIN_003:
        1. Navigate to login page
        2. Enter valid email address
        3. Enter invalid password
        4. Click Login button
        5. Assert error message 'Invalid email or password' is displayed and user remains on login page
        """
        login_page = LoginPage(driver)

        # Step 1: Navigate to login page
        login_page.go_to_login_page()
        assert driver.current_url == login_url, "Should be on login page URL"
        assert login_page.is_login_fields_visible(), "Login fields must be visible"

        # Step 2: Enter valid email address
        assert login_page.enter_email(test_email), f"Email field should contain '{test_email}'"

        # Step 3: Enter invalid password
        assert login_page.enter_password(test_wrong_password), "Password field should be masked"

        # Step 4: Click Login button
        login_page.click_login()

        # Step 5: Assert error message and user remains on login page
        assert login_page.is_error_message_displayed("Invalid email or password"), "Error message must be displayed"
        assert driver.current_url == login_url, "User should remain on login page after failed login"
        assert not login_page.is_redirected_to_dashboard(), "User must NOT be redirected to dashboard"
