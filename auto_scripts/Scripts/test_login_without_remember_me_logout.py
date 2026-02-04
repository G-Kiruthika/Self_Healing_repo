# Selenium Test Script for TC_LOGIN_008: Login without 'Remember Me' and verify logout after browser restart
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage
import time

# Test Data
LOGIN_URL = "https://app.example.com/login"
VALID_EMAIL = "testuser@example.com"
VALID_PASSWORD = "ValidPass123!"

@pytest.mark.usefixtures("driver_init")
class TestLoginWithoutRememberMeLogout:
    def test_login_without_remember_me_logout(self, driver):
        """
        TC_LOGIN_008: Login with valid credentials, leave 'Remember Me' unchecked, close and restart browser, verify user is logged out.
        Steps:
        1. Navigate to login page
        2. Enter valid credentials
        3. Leave 'Remember Me' unchecked
        4. Click login
        5. Assert dashboard is displayed
        6. Close and restart browser
        7. Navigate to application
        8. Assert user is logged out and redirected to login page
        """
        login_page = LoginPage(driver)
        # Step 1: Navigate to login page
        login_page.go_to_login_page()
        assert login_page.is_login_fields_visible(), "Login fields are not visible on the login page."
        # Step 2: Enter valid email and password
        assert login_page.enter_email(VALID_EMAIL), f"Failed to enter email: {VALID_EMAIL}"
        assert login_page.enter_password(VALID_PASSWORD), "Password field is not masked or failed to enter password."
        # Step 3: Ensure 'Remember Me' is unchecked
        checkbox = driver.find_element(*LoginPage.REMEMBER_ME_CHECKBOX)
        if checkbox.is_selected():
            checkbox.click()
        assert not checkbox.is_selected(), "'Remember Me' checkbox should be unchecked."
        # Step 4: Click Login
        login_page.click_login()
        # Step 5: Assert dashboard is displayed (successful login)
        assert login_page.is_redirected_to_dashboard(), "Dashboard is not displayed after login."

        # Step 6: Simulate browser close and restart
        # Save cookies for demonstration (not used since 'Remember Me' is unchecked)
        # cookies = driver.get_cookies()
        driver.quit()
        # Wait briefly to ensure browser is closed
        time.sleep(2)

        # Step 7: Restart browser and navigate to application
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        new_driver = webdriver.Chrome(options=options)
        new_driver.implicitly_wait(10)
        login_page_after_restart = LoginPage(new_driver)
        login_page_after_restart.go_to_login_page()
        # Step 8: Assert user is logged out and redirected to login page
        assert login_page_after_restart.is_logged_out(), "User should be logged out and see the login page after browser restart."
        new_driver.quit()

# Pytest fixture for driver initialization and cleanup
def pytest_addoption(parser):
    parser.addoption(
        "--headless", action="store_true", default=False, help="Run browser in headless mode"
    )

@pytest.fixture(scope="function")
def driver_init(request):
    headless = request.config.getoption("--headless")
    options = Options()
    if headless:
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    try:
        driver.quit()
    except Exception:
        pass
