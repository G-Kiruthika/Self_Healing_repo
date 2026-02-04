# Test Script for TC_LOGIN_007: Login with 'Remember Me' and session persistence
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auto_scripts.Pages.LoginPage import LoginPage
import time

@pytest.mark.usefixtures('driver_init')
class TestLoginRememberMeSessionPersistence:
    @pytest.fixture(scope="class")
    def driver_init(self, request):
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        request.cls.driver = driver
        yield
        driver.quit()

    def test_login_remember_me_session_persistence(self):
        """
        TC_LOGIN_007: End-to-end login flow with 'Remember Me' and session persistence validation.
        Steps:
        1. Navigate to the login page.
        2. Enter valid email and password.
        3. Check the 'Remember Me' checkbox.
        4. Click on the Login button.
        5. Close and restart the browser, then navigate to the application.
        6. Verify user remains logged in and is automatically redirected to dashboard without login prompt.
        Acceptance Criteria: SCRUM-91
        """
        EMAIL = "testuser@example.com"
        PASSWORD = "ValidPass123!"
        LOGIN_URL = "https://app.example.com/login"

        # Step 1: Navigate to the login page
        login_page = LoginPage(self.driver)
        login_page.go_to_login_page()
        assert self.driver.current_url == LOGIN_URL, "Login page is not displayed."
        assert login_page.is_login_fields_visible(), "Login fields are not visible."

        # Step 2: Enter valid email and password
        assert login_page.enter_email(EMAIL), "Email not entered correctly."
        assert login_page.enter_password(PASSWORD), "Password not entered correctly or field not masked."

        # Step 3: Check the 'Remember Me' checkbox
        assert login_page.check_remember_me(), "'Remember Me' checkbox is not checked."

        # Step 4: Click on the Login button
        login_page.click_login()
        # Wait for redirection
        time.sleep(2)
        assert login_page.is_redirected_to_dashboard(), "User is not redirected to dashboard after login."

        # Step 5: Close and restart the browser, then navigate to the application
        session_cookies = self.driver.get_cookies()
        dashboard_url = self.driver.current_url
        self.driver.quit()

        # Restart browser and restore session
        options = Options()
        options.add_argument('--headless')
        new_driver = webdriver.Chrome(options=options)
        new_driver.get(LOGIN_URL)
        for cookie in session_cookies:
            # Selenium requires domain to be set for add_cookie
            cookie_dict = {k: v for k, v in cookie.items() if k in ['name', 'value', 'domain', 'path', 'expiry', 'secure', 'httpOnly', 'sameSite']}
            if 'expiry' in cookie_dict and cookie_dict['expiry'] is not None and isinstance(cookie_dict['expiry'], float):
                cookie_dict['expiry'] = int(cookie_dict['expiry'])
            try:
                new_driver.add_cookie(cookie_dict)
            except Exception:
                pass  # Some cookies may not be added (e.g., those with missing domain), that's fine
        new_driver.refresh()
        time.sleep(2)

        # Step 6: Verify user remains logged in and is redirected to dashboard
        login_page_reloaded = LoginPage(new_driver)
        assert login_page_reloaded.is_redirected_to_dashboard(), (
            "Session did not persist. User was not redirected to dashboard after browser restart."
        )
        new_driver.quit()
