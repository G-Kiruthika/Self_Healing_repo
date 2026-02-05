# Test Script for TC-LOGIN-002: Invalid Login Flow
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from auto_scripts.Pages.LoginPage import LoginPage

@pytest.fixture(scope="class")
def driver():
    options = Options()
    options.add_argument('--headless')  # Run in headless mode for automation
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

class TestLoginInvalidFlow:
    """
    Test Case TC-LOGIN-002
    1. Navigate to the login page
    2. Enter an unregistered or invalid email address
    3. Enter any password
    4. Click on the Login button
    5. Verify error message: 'Invalid email or password'
    6. Verify user remains on login page
    """
    @pytest.mark.tc_login_002
    def test_invalid_login_flow(self, driver):
        login_page = LoginPage(driver)
        email = "invaliduser@example.com"  # Unregistered/invalid email
        password = "SomePassword123"       # Any password
        # Run the invalid login flow method
        result = login_page.tc_login_002_invalid_login_flow(email, password)
        # Assert that both error message and user remains on login page
        assert result, (
            "[TC-LOGIN-002] Invalid login flow failed: either error message not displayed or user not on login page."
        )
        # Additional explicit assertions for traceability
        login_page.navigate_to_login()
        email_entered = login_page.enter_email(email)
        password_entered = login_page.enter_password(password)
        login_page.click_login()
        assert login_page.is_error_message_displayed("Invalid email or password"), (
            "[TC-LOGIN-002] Error message 'Invalid email or password' was not displayed."
        )
        assert login_page.verify_user_stays_on_login_page(), (
            "[TC-LOGIN-002] User was not kept on the login page after invalid login attempt."
        )
