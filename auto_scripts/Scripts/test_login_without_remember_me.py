# Selenium test script for TC_LOGIN_008: Login without 'Remember Me' and verify logout after browser restart
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage
import time

@pytest.mark.usefixtures("driver_init")
class TestLoginWithoutRememberMe:
    @pytest.fixture(scope="class")
    def valid_credentials(self):
        return {
            "email": "testuser@example.com",
            "password": "ValidPass123!"
        }

    def test_login_without_remember_me_and_verify_logout(self, driver, valid_credentials):
        """
        TC_LOGIN_008: Login with valid credentials, do NOT check 'Remember Me', close and restart browser, verify user is logged out.
        Steps:
        1. Navigate to login page
        2. Enter valid email and password
        3. Ensure 'Remember Me' is unchecked
        4. Click Login button
        5. Close and restart browser (handled in test)
        6. Navigate to app
        7. Assert user is redirected to login page
        """
        login_page = LoginPage(driver)
        # Step 1-4: Login without Remember Me
        login_success = login_page.login_without_remember_me(valid_credentials["email"], valid_credentials["password"])
        assert login_success, "User should be redirected to dashboard after login (without Remember Me)"
        # Save cookies (for later, if needed)
        cookies = driver.get_cookies()

        # Step 5: Close and restart browser
        driver.quit()
        time.sleep(2)  # Ensure browser is fully closed
        # Re-initialize the WebDriver (Chrome assumed)
        options = Options()
        options.add_argument('--headless')
        new_driver = webdriver.Chrome(options=options)
        new_driver.implicitly_wait(10)
        try:
            # Step 6: Navigate to login page
            login_page_new = LoginPage(new_driver)
            # Step 7: Verify user is logged out and sees login page
            is_logged_out = login_page_new.verify_logged_out_after_restart()
            assert is_logged_out, "User should be logged out and see the login page after browser restart when 'Remember Me' is unchecked."
        finally:
            new_driver.quit()

# Pytest fixture for driver initialization (standard pattern)
@pytest.fixture(scope="class")
def driver_init(request):
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    request.cls.driver = driver
    yield driver
    driver.quit()
